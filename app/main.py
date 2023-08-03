import datetime as dt
from math import trunc

import plotly.graph_objects as go
import streamlit as st
from mortgage_repayment_calculator.account import Value
from mortgage_repayment_calculator.app import simulation
from mortgage_repayment_calculator.owed import Expenses, HomeLoan, Interest
from plotly.subplots import make_subplots


def filter_dollar_dict(x=None, y=None):
    check = {x_i: y_i for x_i, y_i in zip(x, y)}
    new_x = list(filter(lambda x: check[x] > 0, x))
    new_y = [check[x_i] for x_i in new_x]
    return {"x": new_x, "y": new_y}


def main():
    st.set_page_config(layout="wide")

    with st.expander("Simulation Settings"):
        (
            house_price,
            deposit,
            extra_repayments,
            payment_schedule,
            interest_rate_change_schedule,
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
            capital_gains_schedule,
        ) = simulation.settings()

    button_pressed = st.button(
        "Run Simulation",
        type="primary",
        use_container_width=True,
    )

    if button_pressed:
        if shared_equity is not None:
            mortgage = HomeLoan(house_price - deposit - shared_equity.balance)
        else:
            mortgage = HomeLoan(house_price - deposit)

        interest = Interest(daily_rate_function=interest_rate_change_schedule)
        expenses = Expenses(expenses_monthly, expense_rate_change_schedule)
        counter = -1
        # for date in payment_schedule:
        date = dt.date.today()

        def balance_function() -> float:
            return (
                mortgage.balance.total_dollars
                + interest.balance.total_dollars
                + (
                    shared_equity.balance.total_dollars
                    if shared_equity is not None
                    else 0
                )
            )

        while (
            balance_function() > 0
            and counter < payment_schedule.total_number_of_days * 2
        ) or date < payment_schedule.end_date:
            counter += 1
            date += dt.timedelta(days=1)

            expenses.increase_expenses(date)

            if offset_account is None:
                interest.add_interest(date, mortgage.balance)
            else:
                interest.add_interest(
                    date, mortgage.balance - offset_account.balance
                )

            if counter % transaction_salary_frequency == 0:
                transaction_account.deposit(date, transaction_salary_amount)

            # deposit money into the offset account
            if offset_account is not None:
                if (
                    counter % offset_deposit_schedule == 0
                    and offset_account.balance.total_cents
                    < mortgage.balance.total_cents
                ):
                    withdrew = transaction_account.withdraw(
                        date, offset_deposit_amount
                    )
                    offset_account.deposit(date, withdrew)

            # at the end of the month pay all expenses
            if (date + dt.timedelta(days=1)).month != date.month:
                expenses.add_expenses()
                total_expenses = expenses.balance
                to_pay_expenses: Value = transaction_account.withdraw(
                    date, total_expenses
                )
                if to_pay_expenses.total_cents < total_expenses.total_cents:
                    if offset_account is not None:
                        to_pay_expenses += offset_account.withdraw(
                            date, total_expenses - to_pay_expenses
                        )
                    expenses.make_payment(date, to_pay_expenses)
                else:
                    expenses.make_payment(date, to_pay_expenses)

            if offset_account is not None:
                offset_account.collect_fees(date, transaction_account)

            # increase salary at the end of the financial year
            if date.day == 1 and date.month == 7:
                salary_increase = salary_percentage_increase() / 100
                transaction_salary_amount += Value(
                    trunc(
                        transaction_salary_amount.total_cents
                        * (salary_increase)
                    )
                )
                if offset_deposit_amount is not None:
                    offset_deposit_amount += Value(
                        trunc(
                            offset_deposit_amount.total_cents
                            * (salary_increase)
                        )
                    )

            if counter % transaction_salary_frequency == 0:
                if (
                    mortgage.balance.total_dollars > 0
                    or interest.balance.total_dollars > 0
                ):
                    if interest.balance.total_cents > 0:
                        interest.make_payment(
                            date,
                            transaction_account.withdraw(
                                date, interest.balance
                            ),
                        )
                    else:
                        interest.make_payment(date, Value(0))
                    if mortgage.balance.total_cents > 0:
                        home_payment = mortgage.required_payment(
                            payment_schedule, transaction_salary_frequency
                        )
                        if offset_account is not None:
                            if (
                                offset_account.balance.total_cents
                                < mortgage.balance.total_cents
                            ):
                                withdrew = transaction_account.withdraw(
                                    date, home_payment + extra_repayments
                                )
                                if (
                                    withdrew.total_cents
                                    < home_payment.total_cents
                                ):
                                    withdrew += offset_account.withdraw(
                                        date, home_payment - withdrew
                                    )
                            else:
                                withdrew = offset_account.withdraw(
                                    date, home_payment + extra_repayments
                                )
                        else:
                            withdrew = transaction_account.withdraw(
                                date, home_payment + extra_repayments
                            )

                        change = mortgage.make_payment(date, withdrew)
                        if change.total_dollars > 0:
                            transaction_account.balance += change
                    else:
                        mortgage.make_payment(date, Value(0))
            else:
                interest.make_payment(date, Value(0))
                mortgage.make_payment(date, Value(0))

            if shared_equity is not None:
                shared_equity.add_capital_gains(date)
                if (
                    shared_equity.balance.total_cents > 0
                    and (date + dt.timedelta(days=1)).month != date.month
                ):
                    required_minimum_repayment = Value(
                        trunc(
                            max(
                                1000000,
                                trunc(
                                    shared_equity.balance.total_cents * 0.05
                                ),
                            )
                        )
                    )

                    if (
                        transaction_account.balance.total_cents
                        >= required_minimum_repayment.total_cents
                    ):
                        payment = transaction_account.withdraw(
                            date, required_minimum_repayment
                        )

                        if offset_account is not None:
                            if (
                                offset_account.balance.total_cents
                                > mortgage.balance.total_cents
                            ):
                                payment += offset_account.withdraw(
                                    date,
                                    offset_account.balance - mortgage.balance,
                                )

                        shared_equity.make_payment(date, payment)
                    else:
                        shared_equity.make_payment(date, Value(0))
                else:
                    shared_equity.make_payment(date, Value(0))

        # transaction account
        plot_transaction_withdrawals = go.Scatter(
            filter_dollar_dict(
                **transaction_account.withdrawal_log.as_xy_dollar_dict()
            ),
            showlegend=False,
        )
        plot_transaction_deposits = go.Scatter(
            filter_dollar_dict(
                **transaction_account.deposit_log.as_xy_dollar_dict()
            ),
            showlegend=False,
        )
        plot_transaction_balance = go.Scatter(
            filter_dollar_dict(
                **transaction_account.balance_log.as_xy_dollar_dict()
            ),
            showlegend=False,
        )

        # offset account deposit, withdrawals and balance
        if offset_account is not None:
            plot_offset_account_deposit_log = go.Scatter(
                filter_dollar_dict(
                    **offset_account.deposit_log.as_xy_dollar_dict()
                ),
                showlegend=False,
            )
            plot_offset_account_withdraw_log = go.Scatter(
                filter_dollar_dict(
                    **offset_account.withdrawal_log.as_xy_dollar_dict()
                ),
                showlegend=False,
            )
            plot_offset_account_cumulative_fees = go.Scatter(
                **offset_account.cumulative_fee_log.as_xy_dollar_dict(),
                showlegend=False,
            )
            plot_offset_account_balance_log = go.Scatter(
                **offset_account.balance_log.as_xy_dollar_dict(),
                showlegend=False,
            )

        # interest rates, rate change log
        plot_interest_rate_changes = go.Scatter(
            **interest_rate_change_schedule.yearly_rate_change_log.as_xy_dict(),
            showlegend=False,
        )
        plot_yearly_interest_rate = go.Scatter(
            **interest_rate_change_schedule.yearly_rate_log.as_xy_dict(),
            showlegend=False,
        )
        plot_interest_payments = go.Scatter(
            filter_dollar_dict(**interest.payment_log.as_xy_dollar_dict()),
            showlegend=False,
        )
        plot_cummulative_interst_payments = go.Scatter(
            **interest.cumulative_payment_log.as_xy_dollar_dict(),
            showlegend=False,
        )

        # mortgage repayments
        plot_mortgage_payments = go.Scatter(
            filter_dollar_dict(**mortgage.payment_log.as_xy_dollar_dict()),
            showlegend=False,
        )
        plot_mortgage_cummulative_payments = go.Scatter(
            **mortgage.cumulative_payment_log.as_xy_dollar_dict(),
            showlegend=False,
        )

        # get the payments and rates for the interest rates
        if shared_equity is not None:
            plot_shared_equity_capital_gains_rate_change = go.Scatter(
                **capital_gains_schedule.yearly_rate_change_log.as_xy_dict(),
                showlegend=False,
            )
            plot_shared_equity_capital_gains_rate = go.Scatter(
                **capital_gains_schedule.yearly_rate_log.as_xy_dict(),
                showlegend=False,
            )
            plot_shared_equity_payments = go.Scatter(
                filter_dollar_dict(
                    **shared_equity.payment_log.as_xy_dollar_dict()
                ),
                showlegend=False,
            )
            plot_shared_equity_cumulative_payments = go.Scatter(
                **shared_equity.cumulative_payment_log.as_xy_dollar_dict(),
                showlegend=False,
            )

        # calculate the cummulative payments  for the home
        cummulative_log = interest.cumulative_payment_log.copy()
        for (
            key,
            value,
        ) in mortgage.cumulative_payment_log.items():
            if key in cummulative_log:
                cummulative_log[key] += value
            else:
                cummulative_log[key] = value

        if shared_equity is not None:
            for (
                key,
                value,
            ) in shared_equity.cumulative_payment_log.items():
                if key in cummulative_log:
                    cummulative_log[key] += value

        if offset_account is not None:
            for (
                key,
                value,
            ) in offset_account.cumulative_fee_log.items():
                if key in cummulative_log:
                    cummulative_log[key] += value

        cummulative_log = cummulative_log.as_xy_dollar_dict()

        cummulative_log["x"] = sorted(
            cummulative_log["x"], key=lambda x: cummulative_log["y"]
        )

        cummulative_log["y"] = sorted(cummulative_log["y"])

        plot_cummulative_house_expense = go.Scatter(
            **cummulative_log, showlegend=False
        )

        # expenses
        plot_expense_rate_change_log = go.Scatter(
            **expense_rate_change_schedule.yearly_rate_change_log.as_xy_dict(),
            showlegend=False,
        )
        plot_expense_yearly_rate_log = go.Scatter(
            **expense_rate_change_schedule.yearly_rate_log.as_xy_dict(),
            showlegend=False,
        )
        plot_expense_payments = go.Scatter(
            **expenses.monthly_expenses_log.as_xy_dollar_dict(),
            showlegend=False,
        )
        plot_expenses_cummulative_payments = go.Scatter(
            **expenses.cumulative_payment_log.as_xy_dollar_dict(),
            showlegend=False,
        )

        # now let's create the figures

        if shared_equity is None and offset_account is None:
            fig = make_subplots(
                rows=4,
                cols=4,
                subplot_titles=(
                    "",
                    "Yearly Expenses Rate Change %",
                    "Yearly Interst Rate Change %",
                    "",
                    "Transaction Account Withdrawals $",
                    "Yearly Expenses Inflation Rate %",
                    "Yearly Interest Rates %",
                    "Mortgage Cumulative Repayments $",
                    "Transaction Account Deposits $",
                    "Montly Expenses $",
                    "Mortgage Repayments $",
                    "Interest Cumulative Payments $",
                    "Transaction Account Balance $",
                    "Expenses Cumulative Payments $",
                    "Interest Payments $",
                    "Interest + Mortgage Cumulative Repayments $",
                ),
            )

            fig.add_trace(plot_transaction_withdrawals, row=2, col=1)
            fig.add_trace(plot_transaction_deposits, row=3, col=1)
            fig.add_trace(plot_transaction_balance, row=4, col=1)

            fig.add_trace(plot_expense_rate_change_log, row=1, col=2)
            fig.add_trace(plot_expense_yearly_rate_log, row=2, col=2)
            fig.add_trace(plot_expense_payments, row=3, col=2)
            fig.add_trace(plot_expenses_cummulative_payments, row=4, col=2)

            fig.add_trace(plot_interest_rate_changes, row=1, col=3)
            fig.add_trace(plot_yearly_interest_rate, row=2, col=3)
            fig.add_trace(plot_mortgage_payments, row=3, col=3)
            fig.add_trace(plot_interest_payments, row=4, col=3)

            fig.add_trace(plot_mortgage_cummulative_payments, row=2, col=4)
            fig.add_trace(plot_cummulative_interst_payments, row=3, col=4)
            fig.add_trace(plot_cummulative_house_expense, row=4, col=4)

        elif shared_equity is None:
            fig = make_subplots(
                rows=4,
                cols=5,
                subplot_titles=(
                    "",
                    "Offset Account Withdrawals $",
                    "Yearly Expense Rate Change %",
                    "",
                    "Mortgage Payments $",
                    "Transaction Account Withdrawals $",
                    "Offset Account Deposits $",
                    "Yearly Expense Inflation Rate %",
                    "Yearly Interest Rate Change %",
                    "Mortgage Cumulative Payments $",
                    "Transaction Account Deposits $",
                    "Offset Account Balance $",
                    "Monthly Expenses $",
                    "Interest Rate %",
                    "Interest Cumulative Payments $",
                    "Transaction Account $",
                    "Offset Account Cumulative Fees $",
                    "Expenses Cumulative Payments $",
                    "Iterest Payments $",
                    "Interest + Mortgage + Offset Account Cumulative Payments",
                ),
            )

            fig.add_trace(plot_transaction_withdrawals, row=2, col=1)
            fig.add_trace(plot_transaction_deposits, row=3, col=1)
            fig.add_trace(plot_transaction_balance, row=4, col=1)

            fig.add_trace(plot_offset_account_withdraw_log, row=1, col=2)
            fig.add_trace(plot_offset_account_deposit_log, row=2, col=2)
            fig.add_trace(plot_offset_account_balance_log, row=3, col=2)
            fig.add_trace(plot_offset_account_cumulative_fees, row=4, col=2)

            fig.add_trace(plot_expense_rate_change_log, row=1, col=3)
            fig.add_trace(plot_expense_yearly_rate_log, row=2, col=3)
            fig.add_trace(plot_expense_payments, row=3, col=3)
            fig.add_trace(plot_expenses_cummulative_payments, row=4, col=3)

            fig.add_trace(plot_interest_rate_changes, row=2, col=4)
            fig.add_trace(plot_yearly_interest_rate, row=3, col=4)
            fig.add_trace(plot_interest_payments, row=4, col=4)

            fig.add_trace(plot_mortgage_payments, row=1, col=5)
            fig.add_trace(plot_mortgage_cummulative_payments, row=2, col=5)
            fig.add_trace(plot_cummulative_interst_payments, row=3, col=5)
            fig.add_trace(plot_cummulative_house_expense, row=4, col=5)
        elif offset_account is None:
            fig = make_subplots(
                rows=4,
                cols=5,
                subplot_titles=(
                    "",
                    "Shared Equity Capital Gains Rate Change %",
                    "Yearly Expense Rate Change %",
                    "",
                    "Mortgage Payments $",
                    "Transaction Account Withdrawals $",
                    "Shared Equity Capital Gains Rate %",
                    "Yearly Expense Inflation Rate %",
                    "Yearly Interest Rate Change %",
                    "Mortgage Cumulative Payments $",
                    "Transaction Account Deposits $",
                    "Shared Equity Payments $",
                    "Monthly Expenses $",
                    "Interest Rate %",
                    "Interest Cumulative Payments $",
                    "Transaction Account $",
                    "Shared Equity Cumulative Payments $",
                    "Expenses Cumulative Payments $",
                    "Iterest Payments $",
                    "Interest + Mortgage + Offset Account Cumulative Payments",
                ),
            )

            fig.add_trace(plot_transaction_withdrawals, row=2, col=1)
            fig.add_trace(plot_transaction_deposits, row=3, col=1)
            fig.add_trace(plot_transaction_balance, row=4, col=1)

            fig.add_trace(
                plot_shared_equity_capital_gains_rate_change, row=1, col=2
            )
            fig.add_trace(plot_shared_equity_capital_gains_rate, row=2, col=2)
            fig.add_trace(plot_shared_equity_payments, row=3, col=2)
            fig.add_trace(plot_shared_equity_cumulative_payments, row=4, col=2)

            fig.add_trace(plot_expense_rate_change_log, row=1, col=3)
            fig.add_trace(plot_expense_yearly_rate_log, row=2, col=3)
            fig.add_trace(plot_expense_payments, row=3, col=3)
            fig.add_trace(plot_expenses_cummulative_payments, row=4, col=3)

            fig.add_trace(plot_interest_rate_changes, row=2, col=4)
            fig.add_trace(plot_yearly_interest_rate, row=3, col=4)
            fig.add_trace(plot_interest_payments, row=4, col=4)

            fig.add_trace(plot_mortgage_payments, row=1, col=5)
            fig.add_trace(plot_mortgage_cummulative_payments, row=2, col=5)
            fig.add_trace(plot_cummulative_interst_payments, row=3, col=5)
            fig.add_trace(plot_cummulative_house_expense, row=4, col=5)
        else:
            fig = make_subplots(
                rows=4,
                cols=6,
                subplot_titles=(
                    "",
                    "Offset Account Withdrawals $",
                    "Shared Equity Capital Gains Rate Change %",
                    "Yearly Expense Rate Change %",
                    "",
                    "Mortgage Payments $",
                    "Transaction Account Withdrawals $",
                    "Offset Account Deposits $",
                    "Shared Equity Capital Gains Rate %",
                    "Yearly Expense Inflation Rate %",
                    "Yearly Interest Rate Change %",
                    "Mortgage Cumulative Payments $",
                    "Transaction Account Deposits $",
                    "Offset Account Balance $",
                    "Shared Equity Payments $",
                    "Monthly Expenses $",
                    "Interest Rate %",
                    "Interest Cumulative Payments $",
                    "Transaction Account $",
                    "Offset Account Cumulative Fees $",
                    "Shared Equity Cumulative Payments $",
                    "Expenses Cumulative Payments $",
                    "Iterest Payments $",
                    "Interest + Mortgage + Offset Account Cumulative Payments",
                ),
            )

            fig.add_trace(plot_transaction_withdrawals, row=2, col=1)
            fig.add_trace(plot_transaction_deposits, row=3, col=1)
            fig.add_trace(plot_transaction_balance, row=4, col=1)

            fig.add_trace(plot_offset_account_withdraw_log, row=1, col=2)
            fig.add_trace(plot_offset_account_deposit_log, row=2, col=2)
            fig.add_trace(plot_offset_account_balance_log, row=3, col=2)
            fig.add_trace(plot_offset_account_cumulative_fees, row=4, col=2)

            fig.add_trace(
                plot_shared_equity_capital_gains_rate_change, row=1, col=3
            )
            fig.add_trace(plot_shared_equity_capital_gains_rate, row=2, col=3)
            fig.add_trace(plot_shared_equity_payments, row=3, col=3)
            fig.add_trace(plot_shared_equity_cumulative_payments, row=4, col=3)

            fig.add_trace(plot_expense_rate_change_log, row=1, col=4)
            fig.add_trace(plot_expense_yearly_rate_log, row=2, col=4)
            fig.add_trace(plot_expense_payments, row=3, col=4)
            fig.add_trace(plot_expenses_cummulative_payments, row=4, col=4)

            fig.add_trace(plot_interest_rate_changes, row=2, col=5)
            fig.add_trace(plot_yearly_interest_rate, row=3, col=5)
            fig.add_trace(plot_interest_payments, row=4, col=5)

            fig.add_trace(plot_mortgage_payments, row=1, col=6)
            fig.add_trace(plot_mortgage_cummulative_payments, row=2, col=6)
            fig.add_trace(plot_cummulative_interst_payments, row=3, col=6)
            fig.add_trace(plot_cummulative_house_expense, row=4, col=6)

        fig.update_layout(height=1000)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
