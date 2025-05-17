# data/data_processor.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple

class DataProcessor:
    def __init__(self, sequence_length: int = 60):
        self.sequence_length = sequence_length
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
    def preprocess_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, MinMaxScaler]:
        """LSTM 모델을 위한 데이터 전처리"""
        # 결측치 처리
        df = df.dropna()
        
        # 종가 데이터 추출 및 정규화
        data = df['close'].values.reshape(-1, 1)
        data = self.scaler.fit_transform(data)
        
        x, y = [], []
        for i in range(len(data) - self.sequence_length):
            x.append(data[i:i + self.sequence_length])
            y.append(data[i + self.sequence_length])
            
        x = np.array(x)
        y = np.array(y)
        
        # 데이터가 충분한지 확인
        if len(x) < 10:
            raise ValueError("데이터가 충분하지 않습니다. 더 많은 데이터가 필요합니다.")
        
        # 훈련/테스트 분할 (80/20)
        train_size = int(len(x) * 0.8)
        return x[:train_size], y[:train_size], x[train_size:], y[train_size:], self.scaler
    
    def preprocess_realtime_data(self, df: pd.DataFrame) -> np.ndarray:
        """실시간 데이터 전처리"""
        # 결측치 처리
        df = df.dropna()
        
        if len(df) < self.sequence_length:
            raise ValueError(f"실시간 데이터가 부족합니다. 필요한 데이터 포인트: {self.sequence_length}, 받은 데이터 포인트: {len(df)}")
        
        # 가장 최근 sequence_length 개의 데이터만 사용
        recent_data = df['close'].values[-self.sequence_length:].reshape(-1, 1)
        
        # 이미 학습된 scaler 사용
        scaled_data = self.scaler.transform(recent_data)
        
        # 모델 입력 형식에 맞게 변환 (1, sequence_length, 1)
        return np.array([scaled_data])