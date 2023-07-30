import streamlit as st
from typing import Tuple
from mortgage_repayment_calculator.account import (
    Offset,
    UbankOffset,
    ANZOffset,
    Value,
)


def settings() -> Tuple[Offset, int, Value]:
    st.header("Offset Account")
    use_offset_account = st.selectbox("Use Offset Account", ["True", "False"])
    offset_account = None
    if use_offset_account == "True":
        _, col, _ = st.columns([0.05, 0.9, 0.05])
        with col:
            offset_type = st.selectbox("Provider", ["Ubank", "ANZ"])
            starting_balance = st.number_input(
                "Starting Balance $", value=50000, step=10000
            )
            deposit_schedule = st.number_input(
                "Deposit Frequency (days)", value=15, step=1
            )
            deposit_amount = st.number_input(
                "Deposit Amount $", value=2000, step=100
            )
            if offset_type == "Ubank":
                offset_account = UbankOffset(
                    Value.from_dollars(starting_balance)
                )
            if offset_type == "ANZ":
                offset_account = ANZOffset(
                    Value.from_dollars(starting_balance)
                )

    return offset_account, deposit_schedule, Value.from_dollars(deposit_amount)
