from threading import Lock


class Blockchain:
    def __init__(self):
        self.chain = []
        # Used to add blocks to chain avoiding race conditions
        self.chain_lock = Lock()
        # We use a checkpoint so we dont send the whole chain on consensus algorithm
        self.checkpoint = 0

    def add_block_to_chain(self, block):
        self.chain_lock.acquire()
        try:
            self.chain.append(block)
        finally:
            self.chain_lock.release()

    def last_block(self):
        self.chain_lock.acquire()
        ch = self.chain[-1]
        self.chain_lock.release()
        return ch

    def get_from_checkpoint(self):
        self.chain_lock.acquire()
        ch = self.chain[self.checkpoint :]
        self.chain_lock.release()
        return ch

    def update_chain(self, new_chain):
        self.chain_lock.acquire()
        self.chain = new_chain
        self.chain_lock.release()

    def get_new_transactions(self):
        # Returns all the transactions in the chain after the checkpoint
        self.chain_lock.acquire()

        new_blocks = self.get_from_checkpoint()
        self.chain_lock.release()
        ret = []
        for bl in new_blocks:
            ret += bl.listOfTransactions
        return ret

    def dumpit(self):
        ret = ""
        for bl in self.chain:
            ret += bl.previousHash + " " + bl.hash + "\n"

        ret += "Transactions\n"
        for bl in self.chain:
            ret += "["
            for tr in bl.listOfTransactions:
                ret += tr.id + ", "
            ret += "]\n"
        return ret
