import streamlit as st

from mortgage_repayment_calculator import app


def settings():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        payment_schedule, rate_change_schedule = app.settings.loan()

    with col2:
        (
            transaction_account,
            transaction_deposit_frequency,
            transaxtion_deposit_amount,
        ) = app.settings.account()

        (
            offset_account,
            offset_deposit_schedule,
            offset_deposit_amount,
        ) = app.settings.offset_account()

    # transaction_account_settings()
