import datetime as dt

import mortgage_repayment_calculator.app
import numpy as np
import streamlit as st
from mortgage_repayment_calculator import account, owed, plan


def get_coords(dictionary: dict):
    output = {"x": list(dictionary.keys()), "y": list(dictionary.values())}
    if isinstance(output["y"][0], account.Value):
        output["y"] = [y.total_dollars for y in output["y"]]
    return output


def main():
    st.set_page_config(layout="wide")
    col1, col2, col3, col4 = st.columns([0.125, 0.125, 0.5, 0.2])

    with col1:
        st.header("Loan Schedule")

        payment_type = st.selectbox(
            "Payment Type", ["Flat Scheduled", "Tapering", "Max Cap"]
        )

        flat_payments = payment_type == "Flat Scheduled"

        rate_function = (
            mortgage_repayment_calculator.app.get_rate_change_function()
        )

        to_seed = st.selectbox("Use seed", [True, False])

        if to_seed:
            seed = st.number_input("seed", step=1)
            np.random.seed(seed)

    with col2:
        st.header("Loan Information")
        loan_balance = st.number_input("Loan Balance $", value=500000)
        loan_term = st.number_input("Loan Term (Years)", value=30)
        repayment_frequency = st.number_input(
            "Repayment Frequency (Days)", value=14
        )
        max_cap = None
        extra_repayments = 0
        if payment_type != "Max Cap":
            extra_repayments = st.number_input(
                "Extra Repayments ($)", value=0, step=1
            )
        else:
            max_cap = st.number_input("Max Capped Payments", value=0, step=1)

        height = st.number_input("height", step=1, value=900)

        button_pressed = st.button(
            "Run Simulation",
            type="primary",
            use_container_width=True,
        )

    with col3:
        if button_pressed:
            (
                rate_function,
                interest_owed,
                mortgage_owed,
            ) = mortgage_repayment_calculator.app.simulate(
                rate_function,
                owed.Interest(rate_function),
                owed.HomeLoan(
                    total_owed=account.Value.from_dollars(loan_balance)
                ),
                plan.Schedule(
                    start_date=dt.date.today(), plan_years=loan_term
                ),
                repayment_frequency=repayment_frequency,
                extra_repayments=extra_repayments,
                flat_payments=flat_payments,
                max_cap=max_cap,
            )

            mortgage_repayment_calculator.app.plot_simulation(
                rate_function, interest_owed, mortgage_owed, height
            )


if __name__ == "__main__":
    main()
