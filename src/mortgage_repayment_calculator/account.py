from math import trunc
from typing import Self, Tuple


class Value:
    whole_dollars: int
    remaining_cents: int
    total_cents: int

    @classmethod
    def get_dollars_and_cents_from_cents(cls, cents: int) -> Tuple[int, int]:
        cents = trunc(cents)
        total_dollars = trunc(cents / 100)
        remaining_cents = cents - total_dollars * 100
        return total_dollars, remaining_cents

    @classmethod
    def get_dollars_and_cents_from_dollars_float(
        cls, dollars: float
    ) -> Tuple[int, int]:
        return cls.get_dollars_and_cents_from_cents(trunc(dollars * 100))

    @classmethod
    def from_dollars(cls, dollars: float) -> Self:
        return cls(trunc(dollars * 100))

    def __init__(self, total_cents: int):
        total_cents = trunc(total_cents)
        dollars, cents = self.get_dollars_and_cents_from_cents(total_cents)
        self.whole_dollars = dollars
        self.remaining_cents = cents
        self.total_cents = total_cents
        self.total_dollars = total_cents / 100

    def __sub__(self, value: "Value") -> "Value":
        return self.__class__(self.total_cents - value.total_cents)

    def __add__(self, value: "Value") -> "Value":
        return self.__class__(self.total_cents + value.total_cents)

    def __str__(self) -> str:
        return "$%d.%0.2d" % (self.whole_dollars, self.remaining_cents)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, value: "Value") -> bool:
        return self.total_cents == value.total_cents
