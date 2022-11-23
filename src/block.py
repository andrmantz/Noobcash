import datetime
from Crypto.Hash import SHA256


class Block:
    def __init__(self, previousHash):
        self.previousHash = previousHash
        self.timestamp = datetime.datetime.now()
        self.hash = None
        self.nonce = None
        self.listOfTransactions = []

    def myHash(self):
        return SHA256.new(
            (str(self.timestamp) + str(self.previousHash) + str(self.nonce)).encode()
        ).hexdigest()

    def add_transaction(self, transaction):
        # add a transaction to the block
        self.listOfTransactions.append(transaction)

    def to_dict(self):
        d = {
            "previousHash": self.previousHash,
            "timestamp": self.timestamp,
            "hash": self.hash,
            "nonce": self.nonce,
            "listOfTransactions": self.listOfTransactions,
        }
        return d

    def __eq__(self, __o: object):
        return isinstance(__o, Block) and self.hash and self.hash == __o.hash

    def tostr(self, ring):
        ret = f"< , nonce: {self.nonce}, ,\n Transactions:{{\n"
        for tr in self.listOfTransactions:
            ret += f"\t{tr.tostr(ring)}\n"
        ret += "}} >"
