import streamlit as st

def login():

    st.title("Universal Bank Statement Analyzer")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username=="admin" and password=="admin":

            st.session_state["login"]=True

        else:

            st.error("Invalid Login")