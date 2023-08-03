import datetime as dt
from math import trunc
from typing import Callable

from typing_extensions import Self

from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.logs import FloatLog
from mortgage_repayment_calculator.owed.base import Base


class GovernmentSharedEquity(Base):
    daily_capital_gains_function: Callable[[dt.date], float]

    def __init__(
        self,
        starting_balance: Value,
        daily_capital_gains_function: Callable[[dt.date], float],
    ):
        self.daily_capital_gains_function = daily_capital_gains_function
        self.daily_capital_gains_log = FloatLog()
        self.effective_yearly_capital_gains_log = FloatLog()
        super().__init__(starting_balance)

    def add_capital_gains(self, date: dt.date) -> Self:
        daily_capital_gains = self.daily_capital_gains_function(date)
        self.daily_capital_gains_log[date] = daily_capital_gains
        self.effective_yearly_capital_gains_log[date] = (
            daily_capital_gains * 365
        )
        self.balance += Value(
            trunc((self.balance.total_cents) * daily_capital_gains / 100)
        )

    def make_payment(self, date: dt.date, payment: Value) -> Value:
        if (payment.total_dollars >= 10000) and (
            payment.total_cents >= (trunc(self.balance.total_cents * 0.05))
        ):
            return super().make_payment(date, payment)
        else:
            super().make_payment(date, Value(0))
        return payment
