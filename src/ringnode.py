from threading import Lock


class RingNode:
    def __init__(self, id, address, public_key, balance):
        self.id = id
        self.address = address
        self.public_key = public_key
        self.balance = balance
        self.balance_lock = Lock()

    def upd_balance(self, amount):
        with self.balance_lock:
            self.balance += amount

    def todict(self):
        d = {
            "id": self.id,
            "address": self.address,
            "public_key": self.public_key,
            "balance": self.balance,
        }
        return d


class RingNodeList:
    def __init__(self):
        self.nodes = []

    # Add node to the list and return its id
    def add_node(self, address, public_key, id=None, balance=0):
        if not id:
            id = len(self.nodes)
        self.nodes.append(RingNode(id, address, public_key, balance))
        return id

    # Return the addresses of every node except myself
    def get_addresses(self, my_public_key):
        ret = []
        for node in self.nodes:
            if node.public_key != my_public_key:
                ret.append(node.address)
        return ret

    def get_id_by_public_key(self, public_key):
        for i in range(len(self.nodes)):
            if self.nodes[i].public_key == public_key:
                return i
        return -1

    # Gets a transaction object and updates the balances
    # based on transaction outputs
    def do_transaction(self, transaction):
        # outputs = transaction.outputs
        sender = transaction.sender_address
        receiver = transaction.receiver_address
        sender_id = self.get_id_by_public_key(sender)
        receiver_id = self.get_id_by_public_key(receiver)

        if sender_id == -1 or receiver_id == -1:
            return

        self.nodes[sender_id].upd_balance(-transaction.amount)
        self.nodes[receiver_id].upd_balance(transaction.amount)

    # Revert an already done transaction
    def undo_transaction(self, transaction):

        sender = transaction.sender_address
        receiver = transaction.receiver_address
        sender_id = self.get_id_by_public_key(sender)
        receiver_id = self.get_id_by_public_key(receiver)

        self.nodes[sender_id].upd_balance(transaction.amount)
        self.nodes[receiver_id].upd_balance(-transaction.amount)

    def get_balance_by_public_key(self, public_key):
        nid = self.get_id_by_public_key(public_key)
        return self.nodes[nid].balance

    def get_addresses_and_ids(self, my_public_key):
        ret = []
        for node in self.nodes:
            if node.public_key != my_public_key:
                ret.append((node.address, node.id))
            else:
                ret.append(("me", node.id))
        return ret
