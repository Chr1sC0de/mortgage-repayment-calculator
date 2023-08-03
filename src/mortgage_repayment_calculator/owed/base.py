import datetime as dt

from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.logs import ValueLog


class Base:
    def __init__(self, starting_balance: Value):
        assert isinstance(starting_balance, Value)
        self.starting_balance = starting_balance
        self.balance = starting_balance

        self.total_paid = Value(0)

        self.payment_log: ValueLog = ValueLog()
        self.balance_log: ValueLog = ValueLog()
        self.cumulative_payment_log: ValueLog = ValueLog()

    def make_payment(self, date: dt.date, payment: Value) -> Value:
        if payment.total_cents >= self.balance.total_cents:
            actual_payment = self.balance
        else:
            actual_payment = payment

        change = payment - actual_payment

        self.total_paid += actual_payment
        self.balance -= actual_payment
        self.balance_log[date] = self.balance
        self.payment_log[date] = actual_payment
        self.cumulative_payment_log[date] = self.total_paid

        return change
