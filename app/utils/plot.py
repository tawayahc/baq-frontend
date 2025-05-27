import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def plot_selected_columns(
        df: pd.DataFrame
    ):
    if 'time' not in df.columns:
        st.error("❌ DataFrame must contain a 'time' column.")
        return

    end_time = pd.to_datetime(df['time'].max()) + pd.Timedelta(hours=1)
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

def plot_prediction(
        df_list: list[pd.DataFrame],
        x_list: list[str],
        y_list: list[str],
        start_time: pd.Timestamp,
        end_time: pd.Timestamp
    ):
    fig = go.Figure()
    line_types = ['solid', 'dash', 'dash']
    colors = ['#79aef3', '#FF4B4B', '#FFA500']
    marker_symbols = ['circle', 'circle', 'circle']
    marker_symbol_sizes = [5, 5, 5]
    names = ['PM2.5', 'Next 48 Hours Predicted PM2.5', 'Next 1 Hour Predicted PM2.5']
    last_mill_extraction_value = None

    for i, (df, x_col, y_col) in enumerate(zip(df_list, x_list, y_list)):
        if x_col not in df.columns:
            continue
        if y_col not in df.columns:
            continue

        line_type = line_types[i % len(line_types)]
        color = colors[i % len(colors)]
        marker_symbol = marker_symbols[i % len(marker_symbols)]
        marker_symbol_size = marker_symbol_sizes[i % len(marker_symbol_sizes)]
        name = names[i % len(names)]
        
        if not df.empty:
            if i == 0:
                last_mill_extraction_value = df[x_col].iloc[-1]
            
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[y_col],
                mode='lines+markers',
                line=dict(dash=line_type, color=color),
                marker=dict(symbol=marker_symbol, size=marker_symbol_size, color=color),
                name=name
            ))

            last_x = df[x_col].iloc[-1]
            last_y = df[y_col].iloc[-1]
            fig.add_annotation(
                x=last_x,
                y=last_y,
                text=f"{last_y:.2f}",
                showarrow=True,
                arrowhead=1,
                ax=25,
                ay=-25,
                standoff=5,
                xref="x",
                yref="y",
                font=dict(color=color, size=15),
                arrowcolor=color,
            )

    if last_mill_extraction_value is not None:
        fig.add_shape(
            type="line",
            x0=last_mill_extraction_value,
            x1=last_mill_extraction_value,
            y0=0,
            y1=1,
            line=dict(color="#00ae69", width=1, dash="dash"),
            xref="x",
            yref="paper"
        )
        fig.add_annotation(
            x=last_mill_extraction_value,
            y=1,
            text=f"Current Timestamp: {last_mill_extraction_value}",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-40,
            xref="x",
            yref="paper",
            font=dict(color="#00ae69", size=15),
            arrowcolor="#00ae69",
        )

    fig.update_layout(
        xaxis=dict(
            range=[start_time, end_time],
            title="Timestamp"
        ),
        yaxis=dict(
            range=[
                df_list[0][y_list[0]].iloc[-1] * 0.4,
                df_list[0][y_list[0]].iloc[-1] * 1.6
            ],
            title="PM2.5 (µg/m³)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5,
            font=dict(
                color="#808495",
                size=15
            )
        )
    )

    st.plotly_chart(fig, use_container_width=True)
