import datetime as dt
from collections import OrderedDict
from math import trunc
from typing import Callable, Self

from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.plan import Schedule


class House:
    def __init__(self, total_owed: Value):
        assert isinstance(total_owed, Value)
        self.total_owed = total_owed

        self.total_paid = Value(0)
        self.loan_balance = total_owed

        self.payment_log = OrderedDict()
        self.cumulative_payment_log = OrderedDict()

    def make_payment(self, date: dt.date, payment: Value) -> Self:
        if payment.total_cents >= self.loan_balance.total_cents:
            payment = self.loan_balance

        self.total_paid += payment
        self.loan_balance -= payment
        self.payment_log[date] = payment
        self.cumulative_payment_log[date] = self.total_paid
        return self

    def make_scheduled_payment(self, schedule: Schedule, n_days: int = 1):
        return self.make_payment(
            schedule.current_date,
            Value(self.loan_balance.total_cents / schedule.days_left * n_days),
        )


class Interest:
    daily_rate_function: Callable[[dt.date], float]

    def __init__(
        self,
        daily_rate_function: Callable[[dt.date], float],
    ):
        self.total_paid = Value(0)
        self.unpaid_interest = Value(0)
        self.daily_rate_log = OrderedDict()
        self.effective_yearly_rate_log = OrderedDict()
        self.payment_log = OrderedDict()
        self.cumulative_payment_log = OrderedDict()
        self.daily_rate_function = daily_rate_function

    def add_interest(self, date: dt.date, loan_balance: Value) -> Self:
        daily_rate = self.daily_rate_function(date)
        self.daily_rate_log[date] = daily_rate
        self.effective_yearly_rate_log[date] = daily_rate * 365
        self.unpaid_interest += Value(
            trunc(loan_balance.total_cents * daily_rate / 100)
        )
        return self

    def make_payment(self, date: dt.date, payment: Value) -> Self:
        if payment.total_cents >= self.unpaid_interest.total_cents:
            payment = self.unpaid_interest
        self.unpaid_interest -= payment
        self.total_paid += payment
        self.payment_log[date] = payment
        self.cumulative_payment_log[date] = self.total_paid
        return self
