import streamlit as st

def render_sidebar():
    st.sidebar.title("Next 1 Hour PM2.5 Forecast")
    st.sidebar.metric(label="PM2.5", value="N/A µg/m³", delta="N/A µg/m³", delta_color="inverse", border=True)