from mortgage_repayment_calculator.account import Value


class General:
    def __init__(self, initial_amount: Value):
        self.balance = initial_amount

    def withdraw(self, withdrawal: Value) -> Value:
        if withdrawal.total_cents >= self.balance.total_cents:
            self.balance -= withdrawal
            return withdrawal
        withdrawal = Value(self.balance.total_cents)
        self.balance -= withdrawal
        return withdrawal

    def deposit(self, value: Value) -> Value:
        self.balance += value
        return self.balance
