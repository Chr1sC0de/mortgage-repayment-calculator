import datetime as dt
from typing import Tuple

import numpy as np
import streamlit as st

from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.app import rate_change_schedule
from mortgage_repayment_calculator.functions import (
    rate_schedule,
)
from mortgage_repayment_calculator.plan import Schedule


def settings() -> Tuple[Value, Value, Value, Schedule, rate_schedule.Base]:
    st.header("Loan Settings")
    use_random_seed = st.selectbox("Use Random Seed", ["True", "False"])

    if use_random_seed == "True":
        _, col, _ = st.columns([0.05, 0.9, 0.05])
        with col:
            random_seed = st.number_input("Seed", value=0, step=1)
            np.random.seed(random_seed)

    house_price = st.number_input("Home Price $", value=650000, step=10000)
    deposit = st.number_input("Home Deposit $", value=150000, step=10000)
    extra_repayments = st.number_input(
        "Extra Repayments (uses transaction account balance of too much) $",
        value=0,
        step=100,
    )

    house_price = Value.from_dollars(house_price)
    deposit = Value.from_dollars(deposit)
    extra_repayments = Value.from_dollars(extra_repayments)

    loan_years = st.slider(
        "Loan Term (years)", value=30, min_value=1, max_value=40, step=1
    )

    interest_rate_schedule = rate_change_schedule.get(
        starting_yearly_rate_default=7.5,
        std_rate_changes_per_year=3.0,
        average_rate_changes_per_year=3.0,
        base_yearly_rate_title="Base Yearly Rate %",
        avg_num_rate_changes_per_year_title="Average Number of Rate Changes Per Year",
        std_num_rate_change_per_year_title="Standard Deviation of Number"
        + " of Rate Changes Per Year",
    )

    return (
        house_price,
        deposit,
        extra_repayments,
        Schedule(start_date=dt.date.today(), plan_years=loan_years),
        interest_rate_schedule,
    )
