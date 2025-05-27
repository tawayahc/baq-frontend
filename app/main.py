import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from datetime import datetime
from dateutil.relativedelta import relativedelta
from services.data_loader import S3DataLoader
from services.api_client import APIClient

from components.sidebar import render_sidebar

from utils.plot import plot_selected_columns


st.set_page_config(
    page_title="baq dashborad",
    page_icon="☀️",
    layout="wide"
)


RUNNING_RATE = 60
load_dotenv()
loader = S3DataLoader()
api_client = APIClient()


@st.fragment(run_every=RUNNING_RATE)
def fetch_new_data():
    timelabel = datetime.today() - relativedelta(days=1)
    timelabel = timelabel.strftime('%Y_%m_%d')
    raw_data_source = f'webapp-storage/data/raw/raw_data_{timelabel}.csv'
    st.session_state['mockup_data'] = loader.get_data(raw_data_source)

@st.fragment(run_every=RUNNING_RATE)
def display_data():
    st.subheader("Historical Data Table")
    df = st.session_state['mockup_data']
    if df is None or df.empty:
        st.warning("No data available for the selected date.")
        return
    st.dataframe(df, use_container_width=True)
    st.subheader("Historical Data Chart")
    plot_selected_columns(df)


def main():
    st.title("Bangkok Air Quality Dashboard")
    fetch_new_data()
    render_sidebar()

    home_tab, forecast_tab, dashboard_tab, data_tab = st.tabs(
        ["Home", "PM2.5 Prediction", "Dashboard", "Historical Data"]
    )
    
    with home_tab:
        st.header("Welcome to the Bangkok Air Quality Dashboard")

    with forecast_tab:
        st.header("PM2.5 Prediction")
        ss_res = api_client.single_step()
        single_step_pred = (ss_res.get("predictions") or [None])[0]

        ms_res = api_client.multi_step()
        multi_step_pred = [
            pred.get("predicted_value")
            for pred in ms_res.get("predictions", [])
        ]
        st.write("Single Step Prediction:", single_step_pred)
        st.write("Multi Step Prediction:", multi_step_pred)

    with dashboard_tab:
        st.header("Dashboard")
        st.markdown("This section will display various visualizations and insights about air quality and weather data.")
        # dashboard()

    with data_tab:
        st.header("Historical Data")
        display_data()

if __name__ == "__main__":
    main()
