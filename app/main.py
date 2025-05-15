import streamlit as st
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="baq dashborad",
    page_icon="☀️",
    layout="wide"
)

render_sidebar()

st.title("Welcome to the Streamlit App")