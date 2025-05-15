import streamlit as st

def render_sidebar():
    predicted_value = 100
    current_value = 50
    delta = current_value - predicted_value

    st.sidebar.title("Next 1 Hour PM2.5 Forecast")
    st.sidebar.metric(
        label="PM2.5",
        value=f"{predicted_value} µg/m³",
        delta=f"{delta} µg/m³",
        delta_color="inverse",
        border=True
    )