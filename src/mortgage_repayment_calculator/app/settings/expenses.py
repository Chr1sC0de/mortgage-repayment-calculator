from typing import Tuple

import streamlit as st

from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.app import rate_change_schedule
from mortgage_repayment_calculator.functions import rate_schedule


def settings() -> Tuple[Value, rate_schedule.Base]:
    st.header("Monthly Expenses")

    montly_expenses = st.number_input(
        "Monthly Expenses $", value=4000, step=100
    )

    montly_expenses = Value.from_dollars(montly_expenses)

    expenses_rate_change_schedule = rate_change_schedule.get(
        starting_yearly_rate_default=2.0,
        average_rate_changes_per_year=3.0,
        std_rate_changes_per_year=0.1,
        base_yearly_rate_title="Expenses Inflation Rate %",
        avg_num_rate_changes_per_year_title="Average Number of"
        + " Expenses Rate Changes Per Year",
        std_num_rate_change_per_year_title="Standard Deviation of Number"
        + " of Expenses Rate Changes Per Year",
        rate_change_distribution_type_name="Expenses Rate Change Distribution Type",
        avg_change_name="Average Expenses Rate Change Per Change Decision",
        std_change_name="Standard Deviation of Expenses"
        + " Rate Change Per Change Decision",
        avg_change_name_1="Average Expenses Rate Change Per Change Decision"
        + " (Distribution 1)",
        std_change_name_1="Standard Deviation of Expenses Rate Change"
        + " Per Change Decision (Distribution 1)",
        avg_change_name_2="Average Expenses Rate Change Per"
        + " Change Decision (Distribution 2)",
        std_change_name_2="Standard Deviation of Expenses Rate Change"
        + " Per Change Decision (Distribution 2)",
    )

    return montly_expenses, expenses_rate_change_schedule
