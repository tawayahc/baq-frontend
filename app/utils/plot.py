import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def plot_selected_columns(df: pd.DataFrame):
    if 'time' not in df.columns:
        st.error("❌ DataFrame must contain a 'time' column.")
        return

    df['time'] = pd.to_datetime(df['time'])

    end_time = df['time'].max()
    start_time = end_time - pd.Timedelta(days=1)

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    selected_cols = st.multiselect("📌 Select columns to plot:", numeric_cols)

    if not selected_cols:
        st.info("Please select at least one column to plot.")
        return

    fig = go.Figure()
    for col in selected_cols:
        fig.add_trace(go.Scatter(
            x=df['time'],
            y=df[col],
            mode='lines+markers',
            name=col
        ))

    fig.update_layout(
        title="Historical Trends",
        xaxis=dict(
            range=[start_time, end_time],
            title="Time"
        ),
        yaxis=dict(
            title="Value",
        ),
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)