import datetime
import pytz
import time
from entity_interface import EntityInterface
from splitwise import Splitwise
from classes import Transaction


class SplitwiseAccount(EntityInterface):
    def __init__(self):
        super().__init__()
        # Harcoding for now
        self.sObj = Splitwise(
            "5VroAWaqz7NV8TtdosKf3i7LgPwXzTvhnsiyQzwu",
            "Y08bKUj2t8EhmkROq5Vs28wrTU1Ih6pELQxXKY4Z",
            api_key="PGTAd3NRPmXjiZcK8yBKOu6iIMGpwVDKVCpPaMo0",
        )
        self.id = self.sObj.getCurrentUser().getId()
        self.tz = pytz.timezone("America/Los_Angeles")
        self.balance = 0.0

    def get_balance(self):
        return self.sObj.getCurrentUser()

    def get_transactions(self, inp_time):
        transactions = []
        net_balance_delta = 0.0
        update_after = (
            datetime.datetime.fromtimestamp(inp_time, self.tz) if inp_time else None
        )
        for expense in self.sObj.getExpenses(updated_after=update_after, limit=1000):
            is_self_involved = False
            eu = None
            for expense_user in expense.getUsers():
                if expense_user.getId() == self.id:
                    eu = expense_user
                    is_self_involved = True
            if not is_self_involved:
                continue
            ct = time.strptime(expense.getCreatedAt(), "%Y-%m-%dT%H:%M:%S%z")
            ut = time.strptime(expense.getUpdatedAt(), "%Y-%m-%dT%H:%M:%S%z")
            # ct = ct.replace(tzinfo=pytz.utc).astimezone(self.tz)
            # ut = ut.replace(tzinfo=pytz.utc).astimezone(self.tz)
            transaction = Transaction(
                "Splitwise", eu.net_balance, expense.getDescription(), ut, ct
            )
            transactions.append(transaction)
            net_balance_delta += float(eu.net_balance)
        self.balance += net_balance_delta
        return transactions
