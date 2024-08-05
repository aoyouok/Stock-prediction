import tushare as ts
import pandas as pd
import streamlit as st

# 设置Tushare的token
ts.set_token('42f71165e61b55e765d1f96f4ba3751cecfa910d2a88e26172a025a4')  # 替换为你的实际API token
pro = ts.pro_api()

def load_data(ticker, start_date, end_date):
    """获取指定股票代码在时间段内的历史数据"""
    try:
        data = pro.daily(ts_code=ticker, start_date=start_date, end_date=end_date)
        if data.empty:
            raise ValueError(f"无法获取{ticker}的历史数据，可能是因为该股票代码错误。")
        data['trade_date'] = pd.to_datetime(data['trade_date'])
        data = data.sort_values('trade_date')
        data.reset_index(drop=True, inplace=True)
        return data
    except Exception as e:
        st.error(f"获取数据失败: {e}")
        return pd.DataFrame()  # 返回空的数据框

