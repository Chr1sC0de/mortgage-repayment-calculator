import datetime as dt
from collections import OrderedDict
from typing import Dict, Generic, List, TypeVar, Union

from mortgage_repayment_calculator.account import Value

T = TypeVar("T")


class LogTemplate(OrderedDict[dt.date, T], Generic[T]):
    def iget(self, position: int) -> T:
        return list(self.values())[position]

    def get_y(self) -> List[T]:
        return list(self.values())

    def get_x(self) -> List[T]:
        return list(self.keys())

    def as_xy_dict(self) -> Dict[dt.date, Union[dt.date, T]]:
        return {"x": self.get_x(), "y": self.get_y()}


class ValueLog(LogTemplate[Value]):
    def as_xy_dollar_dict(self):
        return {
            "x": self.get_x(),
            "y": [y.total_dollars() for y in self.get_y()],
        }


FloatLog = LogTemplate[float]
