import numpy as np

def preprocess_data(data):
    """处理数据以用于模型训练"""
    data['Prediction'] = data['close'].shift(-30)
    data = data.dropna()  # 去掉NaN值
    X = np.array(data.drop(['Prediction', 'trade_date', 'ts_code'], axis=1))
    y = np.array(data['Prediction'])
    return X, y

