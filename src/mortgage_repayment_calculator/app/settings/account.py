from typing import Tuple

import streamlit as st

from mortgage_repayment_calculator.account import Transaction, Value


def settings() -> Tuple[Transaction, int, Value]:
    st.header("Transaction Account")
    starting_balance = st.number_input(
        "Starting Balance $", value=1000, step=100
    )
    deposit_frequency = st.number_input(
        "Deposit Frequency (days)", value=14, step=1
    )
    deposit_amount = st.number_input("Deposit Amount $", value=2000, step=100)
    transaction_account = Transaction(starting_balance)

    return (
        transaction_account,
        deposit_frequency,
        Value.from_dollars(deposit_amount),
    )
