import streamlit as st


def main():
    from mortgage_repayment_calculator.app import settings

    st.set_page_config(layout="wide")
    with st.expander("Simulation Settings"):
        settings.simulation()

    button_pressed = st.button(
        "Run Simulation",
        type="primary",
        use_container_width=True,
    )
    button_pressed


if __name__ == "__main__":
    main()
