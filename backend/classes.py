class Transaction:
    def __init__(
        self, source_entity, net_balance, merchant, transaction_time, posted_time
    ):
        self.source_entity = source_entity
        self.net_balance = net_balance
        self.merchant = merchant
        self.transaction_time = transaction_time
        self.posted_time = posted_time

    def jsonify(self):
        return {
            "source_entity": self.source_entity,
            "net_balance": self.net_balance,
            "merchant": self.merchant,
            "transaction_time": self.transaction_time,
            "posted_time": self.posted_time,
        }
