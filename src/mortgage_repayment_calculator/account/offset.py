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
        self.cumulative_fee_log = ValueLog()
        super().__init__(initial_amount)

    @abc.abstractmethod
    def collect_fees(self, date: dt.date):
        ...


class ANZOffset(Offset):
    def collect_fees(self, date: dt.date, account: General) -> Self:
        if is_end_of_month(date) and self.balance.total_cents > 0:
            if account.balance.total_cents > 0:
                withdrawal = account.withdraw(date, Value.from_dollars(10))
            elif self.balance.total_cents > 0:
                withdrawal = self.withdraw(date, Value.from_dollars(10))
            else:
                raise Exception(f"Account empty on {date}, no fee taken")
            self.fees_collected += withdrawal
            self.cumulative_fee_log[date] = self.fees_collected
        else:
            self.cumulative_fee_log[date] = self.fees_collected
        return self


class UbankOffset(Offset):
    def collect_fees(self, date: dt.date, account: General) -> Self:
        if is_end_of_year(date) and self.balance.total_cents > 0:
            if account.balance.total_cents > 0:
                withdrawal = account.withdraw(date, Value.from_dollars(250))
            elif self.balance.total_cents > 0:
                withdrawal = self.withdraw(date, Value.from_dollars(250))
            else:
                raise Exception(f"Account empty on {date}, no fee taken")
            self.fees_collected += withdrawal
            self.cumulative_fee_log[date] = self.fees_collected
        else:
            self.cumulative_fee_log[date] = self.fees_collected
        return self
