# models/lstm_model.py
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import Adam

class LSTMModel:
    def __init__(self, sequence_length: int, units: int = 50):
        self.sequence_length = sequence_length
        self.units = units
        self.model = self._build_model()
        
    def _build_model(self) -> Sequential:
        """LSTM 모델 구축"""
        model = Sequential()
        
        # LSTM 레이어
        model.add(LSTM(units=self.units, return_sequences=True, input_shape=(self.sequence_length, 1)))
        model.add(Dropout(0.2))
        
        model.add(LSTM(units=self.units, return_sequences=False))
        model.add(Dropout(0.2))
        
        # 출력 레이어
        model.add(Dense(units=1))
        
        # 모델 컴파일
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
        
        return model
    
    def train(self, x_train: np.ndarray, y_train: np.ndarray, batch_size: int = 32, epochs: int = 100) -> None:
        """모델 학습"""
        self.model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1)
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        """주가 예측"""
        return self.model.predict(x)