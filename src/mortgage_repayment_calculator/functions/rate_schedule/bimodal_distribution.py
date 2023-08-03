import datetime as dt
from typing import Callable

import numpy as np
from typing_extensions import Self

from mortgage_repayment_calculator.functions.rate_schedule import Base


class BimodalDistribution(Base):
    def __init__(
        self,
        starting_yearly_rate: float,
        rate_change_probability: Callable[[], float],
        mean_rate_change_1: float,
        std_rate_change_1: float,
        mean_rate_change_2: float,
        std_rate_change_2: float,
    ):
        self.mean_rate_change_1 = mean_rate_change_1
        self.std_rate_change_1 = std_rate_change_1
        self.mean_rate_change_2 = mean_rate_change_2
        self.std_rate_change_2 = std_rate_change_2
        super().__init__(starting_yearly_rate, rate_change_probability)

    def _rate_change_logic(self, date: dt.date) -> Self:
        self.rate_change = np.random.normal(
            loc=self.mean_rate_change_1, scale=self.std_rate_change_1
        ) + np.random.normal(
            loc=self.mean_rate_change_2, scale=self.std_rate_change_2
        )
        return super()._rate_change_logic(date)
