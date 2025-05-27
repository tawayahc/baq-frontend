import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from datetime import datetime
from dateutil.relativedelta import relativedelta
from services.data_loader import S3DataLoader
from services.api_client import APIClient

from components.sidebar import render_sidebar

from utils.plot import plot_selected_columns, plot_prediction


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
    timelabel = datetime.today() - relativedelta(days=2)
    timelabel = timelabel.strftime('%Y_%m_%d')
    raw_data_source = f'webapp-storage/data/raw/raw_data_{timelabel}.csv'
    df = loader.load_csv(raw_data_source)
    if not df.empty:
        st.session_state['data'] = df

@st.fragment(run_every=RUNNING_RATE)
def display_prediction():
    current_time = st.session_state['data']['time'].max() if 'data' in st.session_state and 'time' in st.session_state['data'].columns else None
    current_value = st.session_state['data']['pm2_5 (μg/m³)'].iloc[-1] if 'data' in st.session_state and 'pm2_5 (μg/m³)' in st.session_state['data'].columns else None

    ss_res = api_client.single_step()
    single_step_pred = (ss_res.get("predictions") or [None])[0]
    st.session_state['single_pred'] = pd.concat(
        [
            st.session_state['single_pred'],
            pd.DataFrame({
                "time": [pd.to_datetime(current_time) + pd.Timedelta(hours=1)],
                "pm2_5 (μg/m³)": [single_step_pred]
            })
        ],
        ignore_index=True
    )

    ms_res = api_client.multi_step()
    multi_step_pred = [
        pred.get("predicted_value")
        for pred in ms_res.get("predictions", [])
    ]
    multi_timestamps = []
    for index in range(len(multi_step_pred)):
        multi_timestamps.append(pd.to_datetime(current_time) + pd.Timedelta(hours=index + 1))
    new_multi_pred = pd.DataFrame({
        "time": multi_timestamps,
        "pm2_5 (μg/m³)": multi_step_pred
    })
    if not st.session_state['multi_pred'].empty:
        st.session_state['multi_pred'] = pd.concat(
            [st.session_state['multi_pred'], new_multi_pred],
            ignore_index=True
        )
    else:
        st.session_state['multi_pred'] = new_multi_pred

    plot_prediction(
        df_list=[
            st.session_state['data'],
            st.session_state['multi_pred'],
            st.session_state['single_pred'],
        ],
        x_list=['time', 'time', 'time'],
        y_list=['pm2_5 (μg/m³)', 'pm2_5 (μg/m³)', 'pm2_5 (μg/m³)'],
        start_time=pd.to_datetime(current_time) - pd.Timedelta(hours=12),
        end_time=pd.to_datetime(current_time) + pd.Timedelta(hours=12)
    )
    
    col1, col2, col3 = st.columns([1, 1, 1], border=True)
    with col1:
        st.metric(
            label="Current Value:",
            value=f"{current_value:.2f}%",
            delta=f"updated on {current_time}",
            delta_color="off"
        )
    with col2:
        st.metric(
            label="Next 1 Hour:",
            value=f"{single_step_pred:.2f}%",
            delta=f"{(single_step_pred - current_value):.2f}%" if not np.isnan(single_step_pred) else "N/A",
            delta_color="inverse"
        )
    with col3:
        if not new_multi_pred.empty:
            st.metric(
                label="Next 48 Hours:",
                value=f"{new_multi_pred['pm2_5 (μg/m³)'].iloc[-1]:.2f}%",
                delta=f"{(new_multi_pred['pm2_5 (μg/m³)'].iloc[-1] - current_value):.2f}%",
                delta_color="inverse"
            )
    

@st.fragment(run_every=RUNNING_RATE)
def display_data():
    st.subheader("Historical Data Table")
    df = st.session_state['data']
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

        st.session_state['single_pred'] = st.session_state['data'][['time', 'pm2_5 (μg/m³)']].tail(1)
        st.session_state['multi_pred'] = pd.DataFrame(columns=['time', 'pm2_5 (μg/m³)'])
        
        display_prediction()

    with dashboard_tab:
        st.header("Dashboard")
        st.markdown("This section will display various visualizations and insights about air quality and weather data.")
        # dashboard()

    with data_tab:
        st.header("Historical Data")
        display_data()

if __name__ == "__main__":
    main()
