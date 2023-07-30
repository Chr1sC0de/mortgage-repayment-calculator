from typing import Callable

import streamlit as st

from mortgage_repayment_calculator.functions.change_occurs import (
    ChangePerYearProbability,
)
from mortgage_repayment_calculator.functions.rate_schedule import (
    BimodalDistribution,
    NormallyDistributed,
)


def change_normally_distributed(
    starting_rate: float,
    rate_change_probability_function: ChangePerYearProbability,
) -> NormallyDistributed:
    mean_rate_change = st.number_input(
        "Average Rate Change Per Change Decision", value=0.25, step=0.01
    )

    std_rate_change = st.number_input(
        "Standard Deviation of Rate Change Per Change Decision",
        value=0.25,
        step=0.01,
    )
    return NormallyDistributed(
        starting_yearly_rate=starting_rate,
        rate_change_probability=rate_change_probability_function,
        mean_rate_change=mean_rate_change,
        std_rate_change=std_rate_change,
    )


def change_bimodal_distribution(
    starting_rate: float,
    rate_change_probability_function: ChangePerYearProbability,
) -> BimodalDistribution:
    mean_rate_change_1 = st.number_input(
        "Average Rate Change Per Change Decision (Distribution 1)",
        value=0.25,
        step=0.01,
    )

    std_rate_change_1 = st.number_input(
        "Standard Deviation of Rate Change Per Change Decision (Distribution 1)",
        value=0.25,
        step=0.01,
    )

    mean_rate_change_2 = st.number_input(
        "Average Rate Change Per Change Decision (Distribution 2)",
        value=-0.25,
        step=0.01,
    )

    std_rate_change_2 = st.number_input(
        "Standard Deviation of Rate Change Per Change Decision (Distribution 2)",
        value=0.25,
        step=0.01,
    )
    return BimodalDistribution(
        starting_yearly_rate=starting_rate,
        rate_change_probability=rate_change_probability_function,
        mean_rate_change_1=mean_rate_change_1,
        std_rate_change_1=std_rate_change_1,
        mean_rate_change_2=mean_rate_change_2,
        std_rate_change_2=std_rate_change_2,
    )
