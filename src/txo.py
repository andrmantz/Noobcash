class Txo:
    def __init__(self, transaction_id, receiver, amount):
        self.tid = transaction_id
        self.receiver = receiver
        self.amount = amount

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, Txo)
            and self.tid == __o.tid
            and self.receiver == __o.receiver
            and self.amount == __o.amount
        )

    def __repr__(self):
        return f"< Tid: {self.tid}, receiver: {self.receiver}, amount: {self.amount}"
