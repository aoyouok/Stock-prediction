import streamlit as st
import pandas as pd
from data_loader import load_data
from data_preprocessing import preprocess_data
from model import train_model, predict
from visualization import plot_data
from utils import generate_detailed_recommendation, STOCK_LIST

def main():
    st.title('股票价格预测平台')
    st.sidebar.header('选择股票')

    # 时间筛选
    start_date = st.sidebar.date_input('开始日期', pd.to_datetime('2014-01-01'))
    end_date = st.sidebar.date_input('结束日期', pd.to_datetime('2024-08-01'))

    # 下拉选择股票代码
    stock_selection = st.sidebar.selectbox(
        '选择股票',
        options=[f'{code} - {name}' for code, name in STOCK_LIST],
        format_func=lambda x: x
    )

    if stock_selection:
        ticker = stock_selection.split(' ')[0]
        stock_name = stock_selection.split(' ')[1]

        st.sidebar.subheader(f'当前选择: {stock_name} ({ticker})')

        # 获取数据
        data = load_data(ticker, start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'))
        if not data.empty:
            st.write(data.tail(10))
            try:
                # 处理数据和训练模型
                X, y = preprocess_data(data)
                model = train_model(X, y)
                prediction = predict(model, data)

                # 显示预测结果
                st.subheader('预测结果')
                future_dates = pd.date_range(start=data['trade_date'].iloc[-1] + pd.Timedelta(days=1), periods=30)
                prediction_df = pd.DataFrame({
                    '预测日期': future_dates,
                    '预测价格': prediction,
                    '价格变化': prediction - data['close'].iloc[-1],
                    '变化幅度 (%)': (prediction - data['close'].iloc[-1]) / data['close'].iloc[-1] * 100
                })

                # 添加中文解释
                prediction_df['价格变化'] = prediction_df['价格变化'].apply(lambda x: f"{x:.2f} 元")
                prediction_df['变化幅度 (%)'] = prediction_df['变化幅度 (%)'].apply(lambda x: f"{x:.2f}%")
                st.write(prediction_df)

                # 显示价格可视化
                st.subheader('价格可视化')
                recent_days = 7  # 例如，显示最近7天的数据
                recent_data = data.tail(recent_days)
                plot_data(data, prediction, stock_name, recent_data=recent_data)

                # 生成并显示建议
                current_price = data['close'].iloc[-1]
                recommendation = generate_detailed_recommendation(prediction, current_price)
                st.subheader('投资建议')
                st.write(recommendation)

            except ValueError as e:
                st.error(f"错误: {e}")

if __name__ == '__main__':
    main()

