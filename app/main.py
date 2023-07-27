import datetime as dt
import streamlit as st
import mortgage_repayment_calculator.app
from mortgage_repayment_calculator import owed, account, plan

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


def get_coords(dictionary: dict):
    output = {"x": list(dictionary.keys()), "y": list(dictionary.values())}
    if isinstance(output["y"][0], account.Value):
        output["y"] = [y.total_dollars for y in output["y"]]
    return output


def main():
    st.set_page_config(layout="wide")
    col1, col2 = st.columns([0.15, 0.85])

    with col1:
        st.header("Repayment Planner")

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

        loan_balance = st.number_input("Loan Balance $", value=600000)
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

        height = st.number_input("height", step=1, value=1000)
        button_pressed = st.button(
            "Run Simulation",
            type="primary",
            use_container_width=True,
        )

    with col2:
        if button_pressed:
            (
                rate_function,
                interest_owed,
                mortgage_owed,
            ) = mortgage_repayment_calculator.app.simulate(
                rate_function,
                owed.Interest(rate_function),
                owed.House(
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
            scheduled_total_payment = {
                date: (interest + mortgage)
                for date, interest, mortgage in zip(
                    interest_owed.payment_log.keys(),
                    interest_owed.payment_log.values(),
                    mortgage_owed.payment_log.values(),
                )
            }

            cummulative_total_payments = {
                date: (interest + mortgage)
                for date, interest, mortgage in zip(
                    interest_owed.cumulative_payment_log.keys(),
                    interest_owed.cumulative_payment_log.values(),
                    mortgage_owed.cumulative_payment_log.values(),
                )
            }

            rates_trace = go.Scatter(
                get_coords(rate_function.yearly_rate_log), showlegend=False
            )
            rate_change_trace = go.Scatter(
                get_coords(rate_function.yearly_rate_change_log),
                showlegend=False,
            )
            interest_payments_trace = go.Scatter(
                get_coords(interest_owed.payment_log), showlegend=False
            )
            total_payments_trace = go.Scatter(
                get_coords(scheduled_total_payment), showlegend=False
            )
            mortgage_payment_trace = go.Scatter(
                get_coords(mortgage_owed.payment_log), showlegend=False
            )
            cummulative_interest_payments_trace = go.Scatter(
                get_coords(interest_owed.cumulative_payment_log),
                showlegend=False,
            )
            cummulative_mortgage_payment_trace = go.Scatter(
                get_coords(mortgage_owed.cumulative_payment_log),
                showlegend=False,
            )
            cummulative_total_payments_trace = go.Scatter(
                get_coords(cummulative_total_payments), showlegend=False
            )
            fig = make_subplots(
                rows=3,
                cols=3,
                shared_xaxes=True,
                subplot_titles=(
                    "Annual Interest Rates",
                    "Rate Changes",
                    "",
                    "Interest Payments",
                    "House Payments",
                    "Total Payments",
                    "Cummulative Interest Payments",
                    "Cummulative House Payments",
                    "Cummulative Total Payment",
                ),
            )
            fig.add_trace(rates_trace, row=1, col=1)
            fig.add_trace(rate_change_trace, row=1, col=2)
            fig.add_trace(interest_payments_trace, row=2, col=1)
            fig.add_trace(mortgage_payment_trace, row=2, col=2)
            fig.add_trace(total_payments_trace, row=2, col=3)
            fig.add_trace(cummulative_interest_payments_trace, row=3, col=1)
            fig.add_trace(cummulative_mortgage_payment_trace, row=3, col=2)
            fig.add_trace(cummulative_total_payments_trace, row=3, col=3)
            fig.update_layout(height=height)
            st.plotly_chart(
                fig,
                use_container_width=True,
            )
    return


if __name__ == "__main__":
    main()
