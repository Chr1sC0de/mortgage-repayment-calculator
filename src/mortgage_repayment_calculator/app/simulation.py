import streamlit as st

from mortgage_repayment_calculator import app


def settings():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        (
            house_price,
            deposit,
            payment_schedule,
            rate_change_schedule,
        ) = app.settings.loan()

    with col2:
        (
            transaction_account,
            transaction_deposit_frequency,
            transaction_deposit_amount,
        ) = app.settings.account()

        (
            offset_account,
            offset_deposit_schedule,
            offset_deposit_amount,
        ) = app.settings.offset_account()

        # app.settings.expenses()

    with col3:
        ...
    # app.settings.shared_equity()

    # transaction_account_settings()
