from math import trunc
from typing import Tuple

import streamlit as st

from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.app import rate_change_schedule
from mortgage_repayment_calculator.functions import rate_schedule
from mortgage_repayment_calculator.owed import GovernmentSharedEquity


def settings(
    house_price: Value,
) -> Tuple[GovernmentSharedEquity, rate_schedule.Base]:
    st.header("Shared Equity")

    use_government_shared_equity = st.selectbox(
        "Apply Government Shared Equity",
        [
            "False",
            "True",
        ],
    )
    government_shared_equity = None
    gains_rate_schedule = None
    if use_government_shared_equity == "True":
        shared_equity = Value(trunc(house_price.total_cents * 0.25))
        st.text(f"The current shared equity is: {shared_equity}")

        gains_rate_schedule = rate_change_schedule.get(
            starting_yearly_rate_default=6.0,
            average_rate_changes_per_year=1.0,
            std_rate_changes_per_year=3.0,
            avg_num_rate_changes_per_year_title="Average Number of "
            + "Captical Gains Rate Changes Per Year",
            std_num_rate_change_per_year_title="Standard Deviation of Number"
            + " of Captical Gains Rate Changes Per Year",
            rate_change_distribution_type_name="Captical Gains"
            + " Rate Change Distribution Type",
            avg_change_name="Average Capital Gains Rate Change Per Change Decision",
            std_change_name="Standard Deviation of Capital Gains"
            + " Rate Change Per Change Decision",
            avg_change_name_1="Average Capital Gains"
            + " Rate Change Per Change Decision (Distribution 1)",
            std_change_name_1="Standard Deviation of Capital Gains Rate Change"
            + " Per Change Decision (Distribution 1)",
            avg_change_name_2="Average Capital Gains"
            + " Rate Change Per Change Decision (Distribution 2)",
            std_change_name_2="Standard Deviation of Capital Gains Rate Change"
            + " Per Change Decision (Distribution 2)",
        )

        government_shared_equity = GovernmentSharedEquity(
            starting_balance=shared_equity,
            daily_capital_gains_function=gains_rate_schedule,
        )

    return government_shared_equity, gains_rate_schedule
