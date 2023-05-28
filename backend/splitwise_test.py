from splitwise_implementation import SplitwiseAccount

if __name__ == "__main__":
    s = SplitwiseAccount(
        "Splitwise", "Splitwise", "5VroAWaqz7NV8TtdosKf3i7LgPwXzTvhnsiyQzwu"
    )
    print(s.get_balance())
    print(s.get_transactions(None))
