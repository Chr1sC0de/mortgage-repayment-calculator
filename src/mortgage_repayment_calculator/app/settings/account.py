from typing import Tuple

import numpy as np
import streamlit as st

from mortgage_repayment_calculator.account import Transaction, Value
from mortgage_repayment_calculator.functions.change_occurs import (
    SalaryPercentageIncrease,
)


def settings() -> Tuple[Transaction, int, Value, SalaryPercentageIncrease]:
    st.header("Transaction Account")
    starting_balance = st.number_input(
        "Starting Balance $", value=10000, step=100
    )
    salary_frequency = st.number_input(
        "Salary Frequency (days)", value=14, step=1
    )
    salary_amount = st.number_input("Salary $", value=4000, step=100)
    transaction_account = Transaction(Value.from_dollars(starting_balance))

    average_percentage_increase_salary_per_year = st.number_input(
        "Average Salary Increase Per Year %", value=2, step=1
    )

    standard_deviation_percentage_increase_salary_per_year = st.number_input(
        "Standard Deviation Salary Change Per Year %", value=0.0, step=0.5
    )

    return (
        transaction_account,
        salary_frequency,
        Value.from_dollars(salary_amount),
        SalaryPercentageIncrease(
            average_percentage_increase_salary_per_year,
            standard_deviation_percentage_increase_salary_per_year,
        ),
    )
