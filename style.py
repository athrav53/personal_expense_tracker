import streamlit as st

def load_css():

    st.markdown("""

    <style>

    .main{
        background-color:#F8F9FA;
    }

    div[data-testid="metric-container"]{
        background:#ffffff;
        border-radius:15px;
        padding:20px;
        box-shadow:2px 2px 10px rgba(0,0,0,0.1);
    }

    h1{
        color:#1565C0;
    }

    </style>

    """, unsafe_allow_html=True)