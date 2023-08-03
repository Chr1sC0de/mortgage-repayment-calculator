import datetime as dt

import numpy as np
import pytest
from mortgage_repayment_calculator import account, owed
from mortgage_repayment_calculator.functions import rate_schedule
from mortgage_repayment_calculator.plan import Schedule

np.random.seed(1)


def test__normal_distribution():
    rate_function = rate_schedule.NormallyDistributed(
        starting_yearly_rate=7.5,
        rate_change_probability=lambda: 1 / (365 / np.random.normal(2, 0)),
        mean_rate_change=0.1,
        std_rate_change=0.5,
    )
    interest_schedule = owed.Interest(rate_function)
    mortgage = owed.HomeLoan(
        starting_balance=account.Value.from_dollars(500000)
    )
    payment_schedule = Schedule(start_date=dt.date.today(), plan_years=15)

    for date in payment_schedule:
        interest_schedule.add_interest(
            date=date, loan_balance=mortgage.balance
        )
        interest_schedule.make_payment(
            date=date,
            payment=interest_schedule.balance,
        )
        mortgage.make_scheduled_payment(schedule=payment_schedule)

    assert mortgage.balance_log.iget(-1).total_cents == 0
    assert (
        mortgage.cumulative_payment_log.iget(-1).total_cents
        == mortgage.starting_balance.total_cents
    )


def test__bimodal_distribution():
    rate_function = rate_schedule.BimodalDistribution(
        starting_yearly_rate=7.5,
        rate_change_probability=lambda: 1 / (365 / np.random.normal(2, 0)),
        mean_rate_change_1=0.125,
        std_rate_change_1=0.8,
        mean_rate_change_2=-0.125,
        std_rate_change_2=0.3,
    )
    interest_schedule = owed.Interest(rate_function)
    mortgage = owed.HomeLoan(
        starting_balance=account.Value.from_dollars(500000)
    )
    payment_schedule = Schedule(start_date=dt.date.today(), plan_years=15)

    for date in payment_schedule:
        interest_schedule.add_interest(
            date=date, loan_balance=mortgage.balance
        )
        interest_schedule.make_payment(
            date=date, payment=interest_schedule.balance
        )
        mortgage.make_scheduled_payment(schedule=payment_schedule)


if __name__ == "__main__":
    pytest.main([__file__])
