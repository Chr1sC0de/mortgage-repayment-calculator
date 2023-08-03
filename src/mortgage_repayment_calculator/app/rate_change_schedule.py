from uuid import uuid4

import streamlit as st

from mortgage_repayment_calculator.app import rate
from mortgage_repayment_calculator.functions import (
    ChangePerYearProbability,
    rate_schedule,
)


def get(
    starting_yearly_rate_default: float = 6.5,
    average_rate_changes_per_year: int = 3,
    std_rate_changes_per_year: float = 3.0,
    base_yearly_rate_title="Base Yearly Rate %",
    avg_num_rate_changes_per_year_title="Average Number of Rate Changes Per Year",
    std_num_rate_change_per_year_title="Standard Deviation of Number"
    + " of Rate Changes Per Year",
    rate_change_distribution_type_name="Rate Change Distribution Type",
    avg_change_name="Average Rate Change Per Change Decision",
    std_change_name="Standard Deviation of Rate Change Per Change Decision",
    avg_change_name_1="Average Rate Change Per Change Decision (Distribution 1)",
    std_change_name_1="Standard Deviation of Rate Change"
    + " Per Change Decision (Distribution 1)",
    avg_change_name_2="Average Rate Change Per Change Decision (Distribution 2)",
    std_change_name_2="Standard Deviation of Rate Change"
    + " Per Change Decision (Distribution 2)",
) -> rate_schedule.Base:
    starting_yearly_rate = st.number_input(
        base_yearly_rate_title,
        value=starting_yearly_rate_default,
        step=0.01,
    )

    rate_changes_per_year = st.number_input(
        avg_num_rate_changes_per_year_title,
        value=average_rate_changes_per_year,
        step=1.0,
    )

    std_rate_changes_per_year = st.number_input(
        std_num_rate_change_per_year_title,
        value=std_rate_changes_per_year,
        step=1.0,
    )

    rate_change_probability = ChangePerYearProbability(
        days=rate_changes_per_year,
        standard_deviation=std_rate_changes_per_year,
    )

    rate_change_distribution_type = st.selectbox(
        rate_change_distribution_type_name,
        ["Normal Distribution", "Bimodal Distribution"],
    )

    _, col, _ = st.columns([0.05, 0.90, 0.05])

    with col:
        if rate_change_distribution_type == "Normal Distribution":
            rate_change_schedule = rate.change_normally_distributed(
                starting_yearly_rate,
                rate_change_probability,
                avg_change_name=avg_change_name,
                std_change_name=std_change_name,
            )

        elif rate_change_distribution_type == "Bimodal Distribution":
            rate_change_schedule = rate.change_bimodal_distribution(
                starting_yearly_rate,
                rate_change_probability,
                avg_change_name_1=avg_change_name_1,
                std_change_name_1=std_change_name_1,
                avg_change_name_2=avg_change_name_2,
                std_change_name_2=std_change_name_2,
            )
        else:
            raise ValueError("distribution not found")

    return rate_change_schedule
