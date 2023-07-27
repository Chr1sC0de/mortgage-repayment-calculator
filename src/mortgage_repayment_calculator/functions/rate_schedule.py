import abc
import datetime as dt
from collections import OrderedDict
from typing import Self

import numpy as np


class Base:
    def __init__(
        self,
        starting_yearly_rate: float,
        daily_rate_change_chance: float,
    ):
        self.current_rate = starting_yearly_rate
        self.starting_rate = starting_yearly_rate

        self.rate_change_chance = daily_rate_change_chance

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
        if self.rate_change_chance >= self.rate_change_check:
            return self._rate_change_logic(date)
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


class NormallyDistributed(Base):
    def __init__(
        self,
        starting_yearly_rate: float,
        rate_change_chance: float,
        mean_rate_change: float,
        std_rate_change: float,
    ):
        self.mean_rate_change = mean_rate_change
        self.std_rate_change = std_rate_change
        super().__init__(starting_yearly_rate, rate_change_chance)

    def _rate_change_logic(self, date: dt.date) -> Self:
        self.rate_change = np.random.normal(
            loc=self.mean_rate_change, scale=self.std_rate_change
        )
        self.yearly_rate_change_log[date] = self.rate_change
        return super()._rate_change_logic(date)


class BimodalDistribution(Base):
    def __init__(
        self,
        starting_yearly_rate: float,
        rate_change_chance: float,
        mean_rate_change_1: float,
        std_rate_change_1: float,
        mean_rate_change_2: float,
        std_rate_change_2: float,
    ):
        self.mean_rate_change_1 = mean_rate_change_1
        self.std_rate_change_1 = std_rate_change_1
        self.mean_rate_change_2 = mean_rate_change_2
        self.std_rate_change_2 = std_rate_change_2
        super().__init__(starting_yearly_rate, rate_change_chance)

    def _rate_change_logic(self, date: dt.date) -> Self:
        self.rate_change = np.random.normal(
            loc=self.mean_rate_change_1, scale=self.std_rate_change_1
        ) + np.random.normal(
            loc=self.mean_rate_change_2, scale=self.std_rate_change_2
        )
        return super()._rate_change_logic(date)
