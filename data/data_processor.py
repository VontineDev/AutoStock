# data/data_processor.py
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple

class DataProcessor:
    def __init__(self, sequence_length: int = 60):
        self.sequence_length = sequence_length
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
    def preprocess_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, MinMaxScaler]:
        """LSTM 모델을 위한 데이터 전처리"""
        data = df['close'].values.reshape(-1, 1)
        data = self.scaler.fit_transform(data)
        
        x, y = [], []
        for i in range(len(data) - self.sequence_length):
            x.append(data[i:i + self.sequence_length])
            y.append(data[i + self.sequence_length])
            
        x = np.array(x)
        y = np.array(y)
        
        train_size = int(len(x) * 0.8)
        return x[:train_size], y[:train_size], x[train_size:], y[train_size:], self.scaler