import datetime as dt

import pytest
from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.functions import ChangePerYearProbability
from mortgage_repayment_calculator.functions.rate_schedule import (
    NormallyDistributed,
)
from mortgage_repayment_calculator.owed.government_shared_equity import (
    GovernmentSharedEquity,
)
from mortgage_repayment_calculator.plan import Schedule


def test__government_shared_equity():
    daily_capital_gains_function = NormallyDistributed(
        starting_yearly_rate=6,
        rate_change_probability=ChangePerYearProbability(
            days=1, standard_deviation=1
        ),
        mean_rate_change=0.0,
        std_rate_change=0,
    )
    government_shared_equity = GovernmentSharedEquity(
        starting_balance=Value.from_dollars(175000),
        daily_capital_gains_function=daily_capital_gains_function,
    )
    pot = Value(0)
    counter = 0
    for date in Schedule(dt.date.today(), 30):
        counter += 1
        government_shared_equity.add_capital_gains(date)
        if counter % 14 == 0:
            pot += Value.from_dollars(600)
        pot = government_shared_equity.make_payment(date, pot)
        if counter % 360 == 0:
            pass
        if government_shared_equity.balance.total_cents == 0:
            break

    assert True


if __name__ == "__main__":
    pytest.main([__file__])
