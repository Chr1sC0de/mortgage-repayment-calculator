from typing import Tuple
from uuid import uuid4

import streamlit as st

from mortgage_repayment_calculator.account import (
    ANZOffset,
    Offset,
    UbankOffset,
    Value,
)


def settings() -> Tuple[Offset, int, Value]:
    st.header("Offset Account")
    use_offset_account = st.selectbox("Use Offset Account", ["True", "False"])
    offset_account = None
    deposit_schedule = None
    deposit_amount = None
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
                "Base Deposit Amount (this scales with salary) $",
                value=2000,
                step=100,
            )
            deposit_amount = Value.from_dollars(deposit_amount)

            if offset_type == "Ubank":
                offset_account = UbankOffset(
                    Value.from_dollars(starting_balance)
                )
            if offset_type == "ANZ":
                offset_account = ANZOffset(
                    Value.from_dollars(starting_balance)
                )

    return offset_account, deposit_schedule, deposit_amount
