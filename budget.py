import streamlit as st

def budget_planner():

    st.subheader("Budget Planner")

    budget = st.number_input(
        "Monthly Budget",
        0,
        1000000
    )

    return budget