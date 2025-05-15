import pandas as pd
import streamlit as st
from components.sidebar import render_sidebar
from services.data_loader import DataLoader
from utils.plot import plot_selected_columns

st.set_page_config(
    page_title="baq dashborad",
    page_icon="☀️",
    layout="wide"
)


RUNNING_RATE = 20
data_loader = DataLoader()


@st.fragment(run_every=RUNNING_RATE)
def fetch_new_data():
    new_index = len(st.session_state['mockup_data'])
    new_row = data_loader.get_data(new_index)
    st.session_state['mockup_data'] = pd.concat(
        [st.session_state['mockup_data'], pd.DataFrame(new_row)],
        ignore_index=True
    )

@st.fragment(run_every=RUNNING_RATE)
def display_data():
    st.subheader("Historical Data Table")
    st.dataframe(st.session_state['mockup_data'], use_container_width=True)

    st.subheader("Historical Data Chart")
    plot_selected_columns(st.session_state['mockup_data'])


def main():
    st.session_state['mockup_data'] = data_loader.load_data(24)
    st.title("Bangkok Air Quality Dashboard")
    render_sidebar()

    home_tab, forecast_tab, dashboard_tab, data_tab = st.tabs(["Home", "PM2.5 Prediction", "Dashboard", "Historical Data"])
    with home_tab:
        st.header("Welcome to the Bangkok Air Quality Dashboard")
    with data_tab:
        st.header("Historical Data")
        fetch_new_data()
        display_data()

if __name__ == "__main__":
    main()