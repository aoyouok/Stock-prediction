from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np


def train_model(X, y):
    """训练线性回归模型"""
    if len(X) == 0 or len(y) == 0:
        raise ValueError("数据不足，无法训练模型")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def predict(model, data):
    """使用训练好的模型进行预测"""
    prediction_days = 30
    future = np.array(data.drop(['Prediction', 'trade_date', 'ts_code'], axis=1))[-prediction_days:]
    prediction = model.predict(future)
    return prediction

