import streamlit as st

from mortgage_repayment_calculator import app


def settings():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        (
            house_price,
            deposit,
            extra_repayments,
            payment_schedule,
            interest_rate_schedule,
        ) = app.settings.loan()

    with col2:
        (
            transaction_account,
            transaction_salary_frequency,
            transaction_salary_amount,
            salary_percentage_increase,
        ) = app.settings.account()

        (
            offset_account,
            offset_deposit_schedule,
            offset_deposit_amount,
        ) = app.settings.offset_account()

    with col3:
        (
            expenses_monthly,
            expense_rate_change_schedule,
        ) = app.settings.expenses()

    with col4:
        (
            shared_equity,
            capital_gains_rate_schedule,
        ) = app.settings.shared_equity(house_price=house_price)

    return (
        house_price,
        deposit,
        extra_repayments,
        payment_schedule,
        interest_rate_schedule,
        transaction_account,
        transaction_salary_frequency,
        transaction_salary_amount,
        salary_percentage_increase,
        offset_account,
        offset_deposit_schedule,
        offset_deposit_amount,
        expenses_monthly,
        expense_rate_change_schedule,
        shared_equity,
        capital_gains_rate_schedule,
    )
