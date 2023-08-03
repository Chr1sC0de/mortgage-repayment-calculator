import datetime as dt
from typing import Callable

import numpy as np
from typing_extensions import Self

from mortgage_repayment_calculator.functions.rate_schedule import Base


class NormallyDistributed(Base):
    def __init__(
        self,
        starting_yearly_rate: float,
        rate_change_probability: Callable[[], float],
        mean_rate_change: float,
        std_rate_change: float,
    ):
        self.mean_rate_change = mean_rate_change
        self.std_rate_change = std_rate_change
        super().__init__(starting_yearly_rate, rate_change_probability)

    def _rate_change_logic(self, date: dt.date) -> Self:
        self.rate_change = np.random.normal(
            loc=self.mean_rate_change, scale=self.std_rate_change
        )
        return super()._rate_change_logic(date)
