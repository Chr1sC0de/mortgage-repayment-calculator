import datetime as dt

import pytest
from mortgage_repayment_calculator import account, owed, plan


@pytest.mark.parametrize("mortgage", range(400000, 600000, 25000))
def test_house_repayment_with_interest(mortgage: float):
    mortgage = account.Value.from_dollars(mortgage)
    interest = owed.Interest(lambda x: 7.5 / 365)
    payment_schedule = plan.Schedule(dt.date.today(), 30)
    home_debt = owed.House(mortgage)
    counter = 0
    day_payment = 30
    for date in payment_schedule:
        counter += 1
        interest.add_interest(date, home_debt.loan_balance)
        if counter % day_payment == 0:
            interest.make_payment(date, interest.unpaid_interest)
            home_debt.make_scheduled_payment(
                payment_schedule, n_days=day_payment
            )
    if interest.unpaid_interest.total_cents > 0:
        interest.make_payment(
            date + dt.timedelta(days=1), interest.unpaid_interest
        )
    if home_debt.loan_balance.total_cents > 0:
        home_debt.make_payment(
            date + dt.timedelta(days=1), home_debt.loan_balance
        )

    assert (
        interest.total_paid.total_cents > home_debt.total_owed.total_cents / 3
    )


@pytest.mark.parametrize("mortgage", range(100000, 525000, 25000))
def test_house_repayment_not_interest(mortgage: float):
    mortgage = account.Value.from_dollars(mortgage)
    payment_schedule = plan.Schedule(dt.date.today(), 30)
    home_debt = owed.House(mortgage)
    for date in payment_schedule:
        home_debt.make_payment(
            date,
            account.Value(
                home_debt.loan_balance.total_cents
                / (payment_schedule.days_left + 1)
            ),
        )

    if home_debt.loan_balance.total_cents > 0:
        home_debt.make_payment(
            date + dt.timedelta(days=1), home_debt.loan_balance
        )
    assert home_debt.total_paid == mortgage
    assert home_debt.loan_balance == account.Value(0)


if __name__ == "__main__":
    pytest.main([__file__])
