# models/lstm_model.py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from typing import Tuple

class LSTMModel:
    def __init__(self, sequence_length: int):
        self.sequence_length = sequence_length
        self.model = self._build_model()
        
    def _build_model(self) -> Sequential:
        """LSTM 모델 생성"""
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(self.sequence_length, 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    
    def train(self, x_train: np.ndarray, y_train: np.ndarray, 
             batch_size: int = 32, epochs: int = 100) -> None:
        """모델 학습"""
        self.model.fit(x_train, y_train, batch_size=batch_size, 
                      epochs=epochs, verbose=0)