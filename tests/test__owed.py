import datetime as dt

import pytest
from mortgage_repayment_calculator import account, owed, plan


@pytest.mark.parametrize("mortgage", range(400000, 600000, 25000))
def test__house_repayment_with_interest(mortgage: float):
    mortgage = account.Value.from_dollars(mortgage)
    interest = owed.Interest(lambda x: 7.5 / 365)
    payment_schedule = plan.Schedule(dt.date.today(), 30)
    home_debt = owed.HomeLoan(mortgage)
    counter = 0
    day_payment = 30
    for date in payment_schedule:
        counter += 1
        interest.add_interest(date, home_debt.balance)
        if counter % day_payment == 0:
            interest.make_payment(date, interest.balance)
            home_debt.make_scheduled_payment(
                payment_schedule, n_days=day_payment
            )
    if interest.balance.total_cents > 0:
        interest.make_payment(date + dt.timedelta(days=1), interest.balance)
    if home_debt.balance.total_cents > 0:
        home_debt.make_payment(date + dt.timedelta(days=1), home_debt.balance)

    assert interest.total_paid.total_cents > home_debt.balance.total_cents / 3


@pytest.mark.parametrize("mortgage", range(100000, 525000, 25000))
def test__house_repayment_not_interest(mortgage: float):
    mortgage = account.Value.from_dollars(mortgage)
    payment_schedule = plan.Schedule(dt.date.today(), 30)
    home_debt = owed.HomeLoan(mortgage)
    for date in payment_schedule:
        home_debt.make_payment(
            date,
            account.Value(
                home_debt.balance.total_cents
                / (payment_schedule.days_left + 1)
            ),
        )

    if home_debt.balance.total_cents > 0:
        home_debt.make_payment(date + dt.timedelta(days=1), home_debt.balance)
    assert home_debt.total_paid == mortgage
    assert home_debt.balance == account.Value(0)


if __name__ == "__main__":
    pytest.main([__file__])
