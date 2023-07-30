import streamlit as st


def simulation():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        loan_settings()


def rate_change_normally_distributed():
    mean_rate_change = st.number_input(
        "Average Rate Change Per Change Decision", value=0.25, step=0.01
    )

    std_rate_change = st.number_input(
        "Standard Deviation of Rate Change Per Change Decision",
        value=0.25,
        step=0.01,
    )
    return mean_rate_change, std_rate_change


def rate_change_bimodal_distribution():
    mean_rate_change_1 = st.number_input(
        "Average Rate Change Per Change Decision (Distribution 1)",
        value=0.25,
        step=0.01,
    )

    std_rate_change_1 = st.number_input(
        "Standard Deviation of Rate Change Per Change Decision (Distribution 1)",
        value=0.25,
        step=0.01,
    )

    mean_rate_change_2 = st.number_input(
        "Average Rate Change Per Change Decision (Distribution 2)",
        value=-0.25,
        step=0.01,
    )

    std_rate_change_2 = st.number_input(
        "Standard Deviation of Rate Change Per Change Decision (Distribution 2)",
        value=0.25,
        step=0.01,
    )
    return (
        mean_rate_change_1,
        std_rate_change_1,
        mean_rate_change_2,
        std_rate_change_2,
    )


def loan_settings():
    st.header("Loan Settings")
    repayment_type = st.selectbox(
        "Repayment Type", ["Scheduled", "Tapering", "Flat"]
    )
    loan_years = st.slider(
        "loan term", value=30, min_value=1, max_value=40, step=1
    )
    starting_yearly_rate = st.number_input(
        "Base Yearly Rate", value=6.5, min_value=0.1, step=0.01
    )

    rate_changes_per_year = st.number_input(
        "Average Number of Rate Changes Per Year",
        value=3,
        min_value=0,
        max_value=20,
        step=1,
    )

    std_rate_changes_per_year = st.number_input(
        "Standard Deviation of Number of Rate Changes Per Year",
        value=3,
        min_value=0,
        max_value=20,
        step=1,
    )

    rate_change_distribution_type = st.selectbox(
        "Rate Change Distribution Type",
        ["Normally Distributed", "Bimodal Distribution"],
    )

    _, col2 = st.columns([0.05, 0.95])

    with col2:
        if rate_change_distribution_type == "Normally Distributed":
            rate_change_normally_distributed()

        if rate_change_distribution_type == "Bimodal Distribution":
            rate_change_bimodal_distribution()

    return (
        {
            "starting_yearly_rate": starting_yearly_rate,
            "rate_change_probability": rate_changes_per_year,
            "std_rate_changes_per_year": std_rate_changes_per_year,
        },
        repayment_type,
        loan_years,
    )
