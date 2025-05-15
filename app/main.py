import pandas as pd
import streamlit as st
from components.sidebar import render_sidebar
from services.data_loader import DataLoader

data_loader = DataLoader()

st.set_page_config(
    page_title="baq dashborad",
    page_icon="☀️",
    layout="wide"
)

@st.fragment(run_every=5)
def fetch_new_data():
    new_index = len(st.session_state['mockup_data'])
    new_row = data_loader.get_data(new_index)
    st.session_state['mockup_data'] = pd.concat(
        [st.session_state['mockup_data'], pd.DataFrame(new_row)],
        ignore_index=True
    )

@st.fragment(run_every=5)
def display_data():
    st.dataframe(st.session_state['mockup_data'], use_container_width=True)

def main():
    st.session_state['mockup_data'] = data_loader.load_data(24)
    st.title("Bangkok Air Quality Dashboard")
    render_sidebar()

    home_tab, dashboard_tab, data_tab = st.tabs(["Home", "Dashboard", "Historical Data"])
    with home_tab:
        st.header("Welcome to the Bangkok Air Quality Dashboard")
        st.write("This dashboard provides real-time air quality data for Bangkok.")
        st.write("Use the sidebar to view the next 1 hour PM2.5 forecast.")
    with data_tab:
        st.header("Historical Data")
        st.write("This is where the historical data will be displayed.")
        fetch_new_data()
        display_data()

if __name__ == "__main__":
    main()