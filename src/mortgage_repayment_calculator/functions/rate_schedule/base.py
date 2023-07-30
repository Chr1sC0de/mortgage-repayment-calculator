import abc
import datetime as dt
from collections import OrderedDict
from typing import Callable

import numpy as np
from typing_extensions import Self


class Base:
    def __init__(
        self,
        starting_yearly_rate: float,
        daily_rate_change_probability: Callable[[], float],
    ):
        self.current_rate = starting_yearly_rate
        self.starting_rate = starting_yearly_rate

        self.rate_change_probability = daily_rate_change_probability

        self.yearly_rate_log = OrderedDict()
        self.yearly_rate_change_log = OrderedDict()
        self.daily_rate_log = OrderedDict()

        self.previous_date = None
        self.current_date = None

        self.rate_change = 0

    @abc.abstractmethod
    def _rate_change_logic(self, date: dt.date) -> Self:
        ...

    def set_rate_change(self, date: dt.date) -> Self:
        if self.rate_change_probability() >= self.rate_change_check:
            self._rate_change_logic(date)
            self.yearly_rate_change_log[date] = self.rate_change
            return self
        self.rate_change = 0
        self.yearly_rate_change_log[date] = self.rate_change
        return self

    def set_current_date(self, date: dt.date) -> Self:
        if self.current_date is not None:
            assert date > self.current_date
        self.current_date = date
        self.previous_date = self.current_date
        self.rate_change_check = np.random.rand()
        return self

    def __call__(self, date: dt.date, external_date_setter: bool = False):
        if not external_date_setter:
            self.set_current_date(date)
            self.set_rate_change(date)

        self.current_rate = np.clip(
            self.current_rate + self.rate_change, 0, None
        )
        self.yearly_rate_log[date] = self.current_rate

        daily_rate = self.current_rate / 365

        self.daily_rate_log[date] = daily_rate

        return daily_rate
