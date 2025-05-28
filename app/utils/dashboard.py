# app/utils/dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def render_dashboard(df: pd.DataFrame):
    # Date Range Picker
    min_date = df['time'].dt.date.min()
    max_date = df['time'].dt.date.max()

    date_selection = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if not (isinstance(date_selection, (list, tuple)) and len(date_selection) == 2):
        st.warning("❗️ Please select a valid date range, not just one date.")
        return

    start_date, end_date = date_selection
    df = df.loc[
        (df['time'].dt.date >= start_date) &
        (df['time'].dt.date <= end_date)
    ].copy()

    if df.empty:
        st.warning("⚠️ No data in selected date range.")
        return

    # KPI Cards
    st.markdown("### 📌 Key Performance Indicators")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Average PM2.5", f"{df['pm2_5_(μg/m³)'].mean():.1f} μg/m³", border=True)
    k2.metric("Average PM10", f"{df['pm10_(μg/m³)'].mean():.0f} μg/m³", border=True)
    k3.metric("Average Temperature", f"{df['temperature_2m_(°C)'].mean():.1f} °C", border=True)
    k4.metric("Average UV Index", f"{df['uv_index'].mean():.1f}", border=True)

    # Trend Charts
    st.markdown("### 📈 Trends Over Time")
    fig_trend1 = px.line(
        df, x="time",
        y=["pm2_5_(μg/m³)", "pm10_(μg/m³)"],
        labels={"value":"µg/m³","variable":"Pollutant"},
        title="PM2.5 & PM10 Over Time"
    )
    st.plotly_chart(fig_trend1, use_container_width=True)

    fig_trend2 = px.line(
        df, x="time",
        y=["temperature_2m_(°C)", "relative_humidity_2m_(%)"],
        title="Temperature & Humidity Over Time"
    )
    st.plotly_chart(fig_trend2, use_container_width=True)

    # Distributions
    st.markdown("### 📊 Distributions")
    var = st.selectbox("Select a Feature to Display Distribution", df.columns.difference(['time', 'hour', 'date'], sort=False))
    col1, col2 = st.columns(2)
    with col1:
        fig_hist = px.histogram(df, x=var, nbins=50, title=f"Histogram of {var}")
        st.plotly_chart(fig_hist, use_container_width=True)
    with col2:
        fig_box = px.box(df, y=var, title=f"Boxplot of {var}")
        st.plotly_chart(fig_box, use_container_width=True)

    # Correlation Matrix
    st.markdown("### 🔗 Correlation Matrix")
    num = df.select_dtypes("number").drop(columns=["hour"], errors="ignore")
    corr = num.corr()
    fig_corr = px.imshow(
        corr, 
        text_auto=".2f", 
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        title="Correlation Between All Numeric Variables",
        width=1000,
        height=1000
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # Time Pattern: PM2.5 Heatmap
    st.markdown("### 🕒 PM2.5 by Hour & Date")
    df['hour'] = df['time'].dt.hour
    df['date'] = df['time'].dt.date
    pivot = df.pivot_table(
        values="pm2_5_(μg/m³)", index="hour", columns="date", aggfunc="mean"
    )
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(pivot, cmap="Reds", ax=ax)
    ax.set_ylabel("Hour of Day")
    st.pyplot(fig)
