import datetime as dt
from math import trunc
from typing import Callable

from typing_extensions import Self

from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.logs import FloatLog
from mortgage_repayment_calculator.owed import Base


class Interest(Base):
    daily_rate_function: Callable[[dt.date], float]

    def __init__(
        self,
        daily_rate_function: Callable[[dt.date], float],
    ):
        self.daily_rate_log = FloatLog()
        self.effective_yearly_rate_log = FloatLog()
        self.daily_rate_function = daily_rate_function
        super().__init__(Value(0))

    def add_interest(self, date: dt.date, loan_balance: Value) -> Self:
        if loan_balance.total_cents < 0:
            loan_balance = Value(0)
        daily_rate = self.daily_rate_function(date)
        self.daily_rate_log[date] = daily_rate
        self.effective_yearly_rate_log[date] = daily_rate * 365
        self.balance += Value(
            trunc(
                (loan_balance.total_cents + self.balance.total_cents)
                * daily_rate
                / 100
            )
        )
        return self
