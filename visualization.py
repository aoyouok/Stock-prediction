import plotly.graph_objs as go
import pandas as pd
import streamlit as st

def plot_data(data, prediction, stock, recent_data=None):
    """绘制股票价格及预测结果的图表"""
    future_dates = pd.date_range(start=data['trade_date'].iloc[-1] + pd.Timedelta(days=1), periods=len(prediction))
    recent_future_dates = pd.date_range(start=data['trade_date'].iloc[-1] + pd.Timedelta(days=1), periods=len(prediction[-7:]))

    fig = go.Figure()

    # 绘制实际价格
    fig.add_trace(go.Scatter(x=data['trade_date'], y=data['close'], mode='lines', name='实际价格'))

    # 绘制预测价格
    fig.add_trace(go.Scatter(x=future_dates, y=prediction, mode='lines', name='预测价格', line=dict(color='red')))

    # 绘制最近几天的分析数据
    if recent_data is not None:
        fig.add_trace(go.Scatter(x=recent_data['trade_date'], y=recent_data['close'], mode='lines', name='最近几天价格', line=dict(color='blue', dash='dash')))

    fig.update_layout(
        title=f'{stock} 股票价格预测',
        xaxis_title='日期',
        yaxis_title='价格',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=14, color='black')
    )

    st.plotly_chart(fig)

    # 绘制最近几天的价格预测图
    if len(prediction) >= 7:
        recent_prediction = prediction[-7:]
        recent_dates = future_dates[-7:]
        fig_recent = go.Figure()

        fig_recent.add_trace(go.Scatter(x=recent_future_dates, y=recent_prediction, mode='lines', name='最近几天预测价格', line=dict(color='orange')))

        fig_recent.update_layout(
            title=f'{stock} 最近7天价格预测',
            xaxis_title='日期',
            yaxis_title='价格',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=14, color='black')
        )

        st.plotly_chart(fig_recent)

