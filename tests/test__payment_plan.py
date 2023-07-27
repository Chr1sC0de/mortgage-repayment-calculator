import datetime as dt

import pytest
from mortgage_repayment_calculator import plan


def test_payment_plan():
    payment_plan = plan.Schedule(dt.date.today(), 30)
    day_list = list(payment_plan)
    assert payment_plan.start_date == day_list[0]
    assert payment_plan.end_date == day_list[-1]
    assert payment_plan.total_number_of_days == len(day_list)
    assert payment_plan.day_number == len(day_list) - 1
    assert payment_plan.days_left == 0


if __name__ == "__main__":
    pytest.main([__file__])
