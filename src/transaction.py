import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from time import time


class Transaction:
    def __init__(
        self,
        sender_address,
        value,
        inputs,
        recipient_address,
        id=None,
        outputs=None,
    ):

        self.sender_address = sender_address
        self.receiver_address = recipient_address
        self.amount = value
        # Case the Transaction was sent to us, so id is already computed
        if id:
            self.id = id
        else:
            # we want the id to be something unique, so we add both current time of transaction and 10 random bytes
            self.id = SHA256.new(
                (sender_address + recipient_address + str(time())).encode()
                + Crypto.Random.get_random_bytes(10)
            ).hexdigest()
        self.inputs = inputs
        self.outputs = outputs if outputs else []
        self.signature = None

    def to_dict(self):
        d = {
            "sender_address": self.sender_address,
            "receiver_address": self.receiver_address,
            "amount": self.amount,
            "id": self.id,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "signature": self.signature,
        }
        return d

    def sign_transaction(self, private):
        """
        Sign transaction with private key
        """
        self.signature = PKCS1_v1_5.new(private).sign(
            SHA256.SHA256Hash(self.id.encode())
        )

    def validate_signature(self):
        return PKCS1_v1_5.new(RSA.importKey(self.sender_address.encode())).verify(
            SHA256.SHA256Hash(self.id.encode()), self.signature
        )

    def __eq__(self, __o: object):
        return isinstance(__o, Transaction) and self.id == __o.id

    def tostr(self, ring):
        return f"< Transaction: {self.id}, sender: {ring.get_id_by_public_key(self.sender_address)}, receiver: {ring.get_id_by_public_key(self.receiver_address)}, amount: {self.amount} >"
