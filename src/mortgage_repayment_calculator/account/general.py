import datetime as dt

from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.logs import ValueLog


class General:
    def __init__(self, initial_amount: Value):
        self.withdrawal_log = ValueLog()
        self.deposit_log = ValueLog()
        self.balance_log = ValueLog()
        self.balance = initial_amount

    def withdraw(self, date: dt.date, withdrawal: Value) -> Value:
        if withdrawal.total_cents >= self.balance.total_cents:
            withdrawal = Value(self.balance.total_cents)
        self.balance -= withdrawal
        if date in self.withdrawal_log:
            self.withdrawal_log[date] += withdrawal
        else:
            self.withdrawal_log[date] = withdrawal
        self.balance_log[date] = self.balance
        return withdrawal

    def deposit(self, date: dt.date, deposit: Value) -> Value:
        self.balance += deposit
        if date in self.deposit_log:
            self.deposit_log[date] += deposit
        else:
            self.deposit_log[date] = deposit
        self.balance_log[date] = self.balance
        return self.balance
