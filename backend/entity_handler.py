from splitwise_implementation import SplitwiseAccount


def fetch_splitwise_transactions(last_updated, maybe_key):
    keys = maybe_key.split(",")
    s = SplitwiseAccount(keys[0], keys[1], keys[2])
    new_transactions = s.get_transactions(last_updated)
    curr_balance = s.get_balance()
    return (curr_balance, new_transactions)
