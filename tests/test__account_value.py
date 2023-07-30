import pytest
from mortgage_repayment_calculator import account


def test__account_value():
    value = account.Value.from_dollars(100.12)
    assert value.whole_dollars == 100
    assert value.remaining_cents == 12
    assert value.total_cents == 10012

    value = account.Value.from_dollars(100.1245)
    assert value.whole_dollars == 100
    assert value.remaining_cents == 12
    assert value.total_cents == 10012

    value1 = account.Value.from_dollars(100.12)
    value2 = account.Value.from_dollars(200.25)
    assert (value1 + value2) == account.Value(30037)

    value1 = account.Value.from_dollars(100.97)
    value2 = account.Value.from_dollars(200.25)
    assert (value1 + value2) == account.Value(30122)

    dollars, cents = account.Value.get_dollars_and_cents_from_cents(10012)
    assert dollars == 100
    assert cents == 12

    dollars, cents = account.Value.get_dollars_and_cents_from_dollars_float(
        100.125
    )
    assert dollars == 100
    assert cents == 12

    dollars, cents = account.Value.get_dollars_and_cents_from_dollars_float(
        -100.25
    )
    assert dollars == -100
    assert cents == -25


if __name__ == "__main__":
    pytest.main([__file__])
