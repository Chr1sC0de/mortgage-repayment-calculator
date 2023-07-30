import abc
import datetime as dt

from typing_extensions import Self

from mortgage_repayment_calculator.account import General, Value
from mortgage_repayment_calculator.functions import (
    is_end_of_month,
    is_end_of_year,
)
from mortgage_repayment_calculator.logs import ValueLog


class Offset(General):
    def __init__(self, initial_amount: Value):
        self.fees_collected = Value(0)
        self.cummulative_fee_log = ValueLog()
        super().__init__(initial_amount)

    @abc.abstractmethod
    def collect_fees(self, date: dt.date):
        ...


class ANZOffset(Offset):
    def collect_fees(self, date: dt.date) -> Self:
        if is_end_of_month(date) and self.balance.total_cents > 0:
            if self.balance.total_cents > 0:
                withdrawal = self.withdraw(Value.from_dollars(10))
                self.fees_collected += Value(withdrawal)
                self.cummulative_fee_log[date] = self.fees_collected
        return self


class UbankOffset(Offset):
    def collect_fees(self, date: dt.date) -> Self:
        if is_end_of_year(date) and self.balance.total_cents > 0:
            if self.balance.total_cents > 0:
                withdrawal = self.withdraw(Value.from_dollars(250))
                self.fees_collected += Value(withdrawal)
                self.cummulative_fee_log[date] = self.fees_collected
        return self
