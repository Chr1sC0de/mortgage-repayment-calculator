import datetime as dt
from typing import Tuple

import numpy as np
import streamlit as st

from mortgage_repayment_calculator.app import rate
from mortgage_repayment_calculator.functions import rate_schedule
from mortgage_repayment_calculator.functions.change_occurs import (
    ChangePerYearProbability,
)
from mortgage_repayment_calculator.plan import Schedule


def settings() -> Tuple[Schedule, rate_schedule.Base]:
    st.header("Loan Settings")
    use_random_seed = st.selectbox("Use Random Seed", ["True", "False"])

    if use_random_seed == "True":
        random_seed = st.number_input("Seed", value=0, step=1)
        np.random.seed(random_seed)

    loan_years = st.slider(
        "loan term", value=30, min_value=1, max_value=40, step=1
    )

    starting_yearly_rate = st.number_input(
        "Base Yearly Rate", value=6.5, min_value=0.1, step=0.01
    )

    rate_changes_per_year = st.number_input(
        "Average Number of Rate Changes Per Year",
        value=3,
        min_value=0,
        max_value=20,
        step=1,
    )

    std_rate_changes_per_year = st.number_input(
        "Standard Deviation of Number of Rate Changes Per Year",
        value=3,
        min_value=0,
        max_value=20,
        step=1,
    )

    rate_change_probability = (
        ChangePerYearProbability(
            days=rate_changes_per_year,
            standard_deviation=std_rate_changes_per_year,
        ),
    )
    rate_change_distribution_type = st.selectbox(
        "Rate Change Distribution Type",
        ["Normal Distribution", "Bimodal Distribution"],
    )

    _, col, _ = st.columns([0.05, 0.90, 0.05])

    with col:
        if rate_change_distribution_type == "Normal Distribution":
            rate_change_schedule = rate.change_normally_distributed(
                starting_yearly_rate, rate_change_probability
            )

        elif rate_change_distribution_type == "Bimodal Distribution":
            rate_change_schedule = rate.change_bimodal_distribution(
                starting_yearly_rate, rate_change_probability
            )
        else:
            raise ValueError("distribution not found")

    return (
        Schedule(start_date=dt.date.today(), plan_years=loan_years),
        rate_change_schedule,
    )
