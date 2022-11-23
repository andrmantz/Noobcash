from Crypto.PublicKey import RSA
from threading import Lock


class Wallet:
    def __init__(self):

        key = RSA.generate(4096)
        self.public_key = key.public_key().exportKey().decode()
        self.private_key = key
        self.address = self.public_key
        self.transactions = []
        # Contains the unspend TXOs(UTXOs) of each wallet
        self.utxos = []
        self.utxos_lock = Lock()

    def to_dict(self):
        # We don't send the private key
        d = {
            "address": self.address,
            "transactions": self.transactions,
        }
        return d

    def balance(self):
        total = 0
        with self.utxos_lock:
            for utxo in self.utxos:
                total += utxo.amount
        return total

    # Calculates transaction inputs and removes the utxos used from the utxos list
    def update_utxos(self, amount):
        total = 0
        utxos_used = []
        with self.utxos_lock:
            for utxo in self.utxos:
                total += utxo.amount
                utxos_used.append(utxo)
                if total >= amount:
                    break
            # There are not enough NBCs
            if total < amount:
                return 0, []

            # We remove the used utxos from the list
            self.utxos = [i for i in self.utxos if i not in utxos_used]
        inputs = [i.tid for i in utxos_used]
        return total, inputs

    def add_transaction_to_wallet(self, transaction):
        # We first need add the transaction to our transactions list
        # Then, add the corresponding outputs to our utxos
        with self.utxos_lock:
            self.transactions.append(transaction)
            outputs = transaction.outputs
            for txo in outputs:
                if txo.receiver == self.public_key:
                    self.utxos.append(txo)
