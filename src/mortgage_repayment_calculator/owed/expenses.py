import datetime as dt
from math import trunc
from typing import Callable

from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.logs import FloatLog, ValueLog
from mortgage_repayment_calculator.owed import Base


class Expenses(Base):
    def __init__(
        self,
        monthly_expenses: Value,
        daily_rate_function: Callable[[dt.date], float],
    ):
        self.monthly_expenses = monthly_expenses
        self.monthly_expenses_log = ValueLog()
        self.daily_rate_log = FloatLog()
        self.effective_yearly_rate_log = FloatLog()
        self.daily_rate_function = daily_rate_function

        super().__init__(Value(0))

    def increase_expenses(self, date):
        daily_rate = self.daily_rate_function(date)
        self.daily_rate_log[date] = daily_rate
        self.effective_yearly_rate_log[date] = daily_rate * 365
        self.monthly_expenses = Value(
            trunc(self.monthly_expenses.total_cents * (1 + daily_rate / 100))
        )

    def make_payment(self, date: dt.date, payment: Value) -> Value:
        self.monthly_expenses_log[date] = payment
        return super().make_payment(date, payment)

    def add_expenses(self):
        self.balance += self.monthly_expenses
