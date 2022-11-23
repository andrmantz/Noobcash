from block import Block
from wallet import Wallet
from blockchain import Blockchain
from transaction import Transaction
from txo import Txo
from ringnode import RingNodeList
from miner import MiningThread
from threading import Lock
import requests
import pickle


class Node:
    def __init__(self, mining_difficulty, capacity_transactions, address, id=None):
        self.id = id if id else 0

        self.blchain = Blockchain()
        self.wallet = Wallet()
        self.current_block = None
        # we use waiting_queue for incoming transactions that are not part of the current block
        self.waiting_queue = []
        self.block_lock = Lock()
        self.miner_lock = Lock()

        # here we store information for every node
        self.ring = RingNodeList()
        self.mining_difficulty = mining_difficulty
        self.capacity_transactions = capacity_transactions
        self.miner = MiningThread(self.mining_difficulty, address)

    def uncommited_transactions(self):
        if self.current_block:
            return self.current_block.listOfTransactions + self.waiting_queue
        return self.waiting_queue

    def create_new_block(self):
        self.current_block = Block(self.blchain.last_block().hash)

    def register_node_to_ring(self, address, public_key):

        return self.ring.add_node(address, public_key)

    def create_transaction(self, receiver, amount):

        total, inputs = self.wallet.update_utxos(amount)
        if not total or not inputs:
            return 1

        transaction = Transaction(self.wallet.public_key, amount, inputs, receiver)

        outputs = [Txo(transaction.id, receiver, amount)]

        if total > amount:
            outputs.append(Txo(transaction.id, self.wallet.address, total - amount))
        transaction.outputs = outputs
        transaction.sign_transaction(self.wallet.private_key)

        # Add it in our wallet
        self.wallet.add_transaction_to_wallet(transaction)
        # Update balances
        self.ring.do_transaction(transaction)
        # Finally, we add the transaction to our queue/block and broadcast it

        self.add_transaction_to_queue(transaction)

        self.broadcast_transaction(transaction)

        return 0

    def broadcast_transaction(self, transaction):
        addresses = self.ring.get_addresses(self.wallet.public_key)
        t_pickle = pickle.dumps(transaction)
        for addr in addresses:
            requests.post(f"http://{addr}/new_transaction", data=t_pickle)

    def accept_transaction(self, transaction: Transaction):
        if not self.validate_transaction(transaction):
            return 1

        # print(transaction.tostr(self.ring))

        # If I am the receiver, add transaction to my wallet
        if transaction.receiver_address == self.wallet.public_key:
            self.wallet.add_transaction_to_wallet(transaction)
        self.ring.do_transaction(transaction)
        self.add_transaction_to_queue(transaction)
        return 0

    def add_transaction_to_queue(self, transaction):
        with self.block_lock:
            if not self.current_block:
                self.create_new_block()
            # We first add higher priority transactions to the block if any
            block_len = self.trigger_queue()
            if block_len < self.capacity_transactions:
                self.current_block.add_transaction(transaction)
            else:
                self.waiting_queue.append(transaction)

            self.check_mine()

    # We use it as a trigger to start adding blocks from the queue to the current block
    def trigger_queue(self):
        num_of_transactions = self.capacity_transactions - len(
            self.current_block.listOfTransactions
        )
        wq = self.waiting_queue[:num_of_transactions].copy()
        for tr in wq:
            self.current_block.add_transaction(tr)
            self.waiting_queue.remove(tr)

        return len(self.current_block.listOfTransactions)

    def validate_transaction(self, transaction):
        return (
            self.ring.get_balance_by_public_key(transaction.sender_address)
            > transaction.amount
            and transaction.validate_signature()
        )

    def accept_block(self, block: Block):
        # There is an incoming block we need to add to chain
        # We first need to check if the new block is valid.
        # If it is not, we start consensus.
        # If it is, we stop mining, because our block wouldn't be valid
        # and remove duplicate transactions.
        fl = False
        if not self.valid_block(block, self.blchain.last_block()):
            # if block.previousHash != self.blchain.last_block().hash:
            #     for bl in self.blchain.chain:
            #         if bl.hash == block.hash:
            #             return

            #         if fl:
            #             self.request_consensus()

            #         if block.previousHash == bl.hash:
            #             fl = True
            #     return
            self.request_consensus()

        # We stop mining, erase our current_block, remove duplicate transactions and trigger queue to start again.
        with self.block_lock:
            self.stop_mine()
            self.miner.clear_miner()
            # Update the waiting queue
            pending = self.uncommited_transactions()
            self.waiting_queue = [
                tr for tr in pending if tr not in block.listOfTransactions
            ]
            self.blchain.add_block_to_chain(block)
            self.create_new_block()
            self.trigger_queue()
            self.check_mine()

    ### Mining Related

    def check_mine(self):
        if len(self.current_block.listOfTransactions) >= self.capacity_transactions:
            self.start_mine()

    def start_mine(self):
        self.miner_lock.acquire()
        # A block is being mined already
        if self.miner.running():
            self.miner_lock.release()
            return 1
        self.miner.set_block(self.current_block)
        self.miner_lock.release()
        ret = self.miner.run()
        return ret

    def stop_mine(self):
        self.miner.stop_mining()

    def broadcast_block(self):
        pickled_block = pickle.dumps(self.current_block)
        addresses = self.ring.get_addresses(self.wallet.public_key)
        for addr in addresses:
            requests.post(f"http://{addr}/new_block", data=pickled_block)

    ### concencus functions
    def valid_block(self, bl, prev_block):
        return (
            bl.previousHash == prev_block.hash
            and bl.hash == bl.myHash()
            and bl.hash.startswith("0" * self.mining_difficulty)
        )

    def valid_chain(self, chain):
        # Case the chain contains only genesis block
        if len(chain) < 2:
            return True

        for i in range(1, len(chain)):
            curr_block = chain[i]
            previous_block = chain[i - 1]
            if not self.valid_block(curr_block, previous_block):
                return False
        return True

    # Inform every node that we run consensus algorithm so they start too
    def request_consensus(self):
        addresses = self.ring.get_addresses(self.wallet.public_key)
        for addr in addresses:
            requests.get(f"http://{addr}/start_consensus")
        self.resolve_conflicts()

    def resolve_conflicts(self):
        """
        * We get every node's chain and add it in our list.
        * We sort the list so the longest chains are in front of the chains list
        * We start looping and keep the first valid.
        """
        # Stop mining and get chain lock
        self.blchain.chain_lock.acquire()
        self.block_lock.acquire()
        self.stop_mine()

        chains = []
        # Get chains
        addresses = self.ring.get_addresses_and_ids(self.wallet.public_key)
        for addr, id in addresses:
            if addr == "me":
                # chains.append((self.blchain.get_from_checkpoint(), id))
                chains.append((self.blchain.chain, id))
                continue
            r = requests.get(f"http://{addr}/chain")
            # We try once again, otherwise we don't get response from that node
            # and consider him unreachable
            if not r.ok:
                r = requests.get(f"http://{addr}/chain")

            if r.ok:
                chains.append((pickle.loads(r.content), id))
        # If there are many chains with the same length, we pick the one that belongs to the smallest id node
        sorted_chains = sorted(chains, key=lambda x: (len(x[0]), x[1]), reverse=True)

        for ch in sorted_chains:
            if self.valid_chain(ch[0]):
                chain, nid = ch
            else:
                print(f"Chain of node {nid} not valid")

        # Now we need to remove all Transactions that are included in the new blocks of
        # the chain from the waiting queue

        old_chain_transactions = self.blchain.get_new_transactions()
        pending_transactions = self.uncommited_transactions()
        self.current_block = None

        # Update the chain
        # self.blchain.chain = self.blchain.get_from_checkpoint() + chain
        self.blchain.chain = chain
        # Get new chain transactions
        new_chain_transactions = self.blchain.get_new_transactions()

        # Now we have to undo any transaction we have done that is not in the new chain
        for tr in old_chain_transactions:
            if tr not in new_chain_transactions:
                self.ring.undo_transaction(tr)

        # We do any transaction in new chain, not in old or pending
        for tr in new_chain_transactions:
            if tr not in old_chain_transactions or tr not in pending_transactions:
                self.ring.do_transaction(tr)

        self.waiting_queue = [
            tr for tr in pending_transactions if tr not in new_chain_transactions
        ]

        # self.blchain.checkpoint = len(self.blchain.chain) - 1

        # We are ready, now we need to create block, and trigger the queue
        self.create_new_block()
        self.trigger_queue()
        self.blchain.chain_lock.release()
        self.block_lock.release()
        print(f"Finised consensus, picked chain of node {nid}")
