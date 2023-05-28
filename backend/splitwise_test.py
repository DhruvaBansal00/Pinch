from splitwise_implementation import SplitwiseAccount

if __name__ == "__main__":
    s = SplitwiseAccount()
    print(s.get_balance())
    print(s.get_transactions(None))
