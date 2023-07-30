import streamlit as st

from mortgage_repayment_calculator.app import simulation


def main():
    st.set_page_config(layout="wide")
    with st.expander("Simulation Settings"):
        simulation.settings()

    button_pressed = st.button(
        "Run Simulation",
        type="primary",
        use_container_width=True,
    )

    if button_pressed:
        ...


if __name__ == "__main__":
    main()
