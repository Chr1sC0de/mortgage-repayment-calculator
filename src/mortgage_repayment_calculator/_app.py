import datetime as dt
from typing import Tuple

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from mortgage_repayment_calculator import account, owed, plan
from mortgage_repayment_calculator.functions import rate_schedule

rate_functions_map = {
    "NormalDistribution": rate_schedule.NormallyDistributed,
    "BimodalDistribution": rate_schedule.BimodalDistribution,
}


def get_coords(dictionary: dict):
    output = {"x": list(dictionary.keys()), "y": list(dictionary.values())}
    if isinstance(output["y"][0], account.Value):
        output["y"] = [y.total_dollars for y in output["y"]]
    return output


def get_rate_change_function():
    rate_function_type = st.selectbox(
        "Rate Function Type",
        options=["NormalDistribution", "BimodalDistribution"],
    )

    starting_yearly_rate = st.number_input("Starting Yearly Rate %", value=7.5)

    average_yearly_rate_change = st.number_input(
        "Average Number of Rate Changes Per Year", value=2, step=1
    )

    standard_deviation_rate_change = st.number_input(
        "Standard Deviation of Rate Changes Per Year", value=5, step=1
    )

    rate_function_constructor = rate_functions_map[rate_function_type]

    def rate_change_chance_function():
        random_rate_change_amount_per_year = np.random.normal(
            average_yearly_rate_change,
            standard_deviation_rate_change,
        )
        if random_rate_change_amount_per_year == 0:
            return 10000000
        return 1 / (365 / random_rate_change_amount_per_year)

    if rate_function_type == "NormalDistribution":
        mean_rate_change = st.number_input(
            "Average Rate Change (Flat %)", value=0.0
        )
        std_rate_change = st.number_input(
            "Rate Change Standard Deviation (Flat %)", value=0.5
        )
        rate_function_kwargs = {
            "starting_yearly_rate": starting_yearly_rate,
            "rate_change_chance": rate_change_chance_function,
            "mean_rate_change": mean_rate_change,
            "std_rate_change": std_rate_change,
        }
    elif rate_function_type == "BimodalDistribution":
        mean_rate_change_1 = st.number_input(
            "Average Rate Change Mode 1", value=0.0
        )
        std_rate_change_1 = st.number_input(
            "Rate Change Standard Deviation Mode 1", value=0.5
        )
        mean_rate_change_2 = st.number_input(
            "Average Rate Change Mode 2", value=0.0
        )
        std_rate_change_2 = st.number_input(
            "Rate Change Standard Deviation Mode 2", value=0.5
        )

        rate_function_kwargs = {
            "starting_yearly_rate": starting_yearly_rate,
            "rate_change_chance": rate_change_chance_function,
            "mean_rate_change_1": mean_rate_change_1,
            "std_rate_change_1": std_rate_change_1,
            "mean_rate_change_2": mean_rate_change_2,
            "std_rate_change_2": std_rate_change_2,
        }

    return rate_function_constructor(**rate_function_kwargs)


def simulate(
    rate_function: rate_schedule.Base,
    interest_owed: owed.Interest,
    mortgage_owed: owed.HomeLoan,
    repayment_schedule: plan.Schedule,
    repayment_frequency: int,
    extra_repayments: int = 0,
    flat_payments: bool = False,
    max_cap: int = None,
) -> Tuple[rate_schedule.Base, owed.Interest, owed.HomeLoan]:
    day_count = 0
    for date in repayment_schedule:
        day_count += 1
        interest_owed.add_interest(
            date=date, loan_balance=mortgage_owed.loan_balance
        )
        if day_count % repayment_frequency == 0:
            if max_cap is None:
                interest_owed.make_payment(
                    date=date, payment=interest_owed.unpaid_interest
                )
                mortgage_owed.make_scheduled_payment(
                    schedule=repayment_schedule,
                    n_days=repayment_frequency,
                    extra_repayment=account.Value.from_dollars(
                        extra_repayments
                    ),
                    flat=flat_payments,
                )
            else:
                payment = account.Value.from_dollars(max_cap)
                left_for_home = payment - interest_owed.unpaid_interest

                if (
                    interest_owed.unpaid_interest.total_dollars
                    <= payment.total_dollars
                ):
                    interest_owed.make_payment(
                        date, interest_owed.unpaid_interest
                    )
                    mortgage_owed.make_payment(date, left_for_home)
                else:
                    interest_owed.make_payment(date, payment)

    if interest_owed.unpaid_interest.total_cents > 0:
        interest_owed.make_payment(
            date=date + dt.timedelta(days=1),
            payment=interest_owed.unpaid_interest,
        )

    if mortgage_owed.loan_balance.total_cents > 0:
        mortgage_owed.make_payment(
            date=date + dt.timedelta(days=1),
            payment=mortgage_owed.loan_balance,
        )

    return rate_function, interest_owed, mortgage_owed


def plot_simulation(
    rate_function: rate_schedule.Base,
    interest_owed: owed.Interest,
    mortgage_owed: owed.HomeLoan,
    height: int,
):
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
        shared_xaxes="all",
        subplot_titles=(
            "",
            "Rate Changes",
            "Annual Interest Rates",
            "Interest Payments",
            "House Payments",
            "Total Payments",
            "Cummulative Interest Payments",
            "Cummulative House Payments",
            "Cummulative Total Payment",
        ),
    )
    fig.add_trace(rate_change_trace, row=1, col=2)
    fig.add_trace(rates_trace, row=1, col=3)
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
