# trading/signal_generator.py
from typing import Tuple, List
import numpy as np

class SignalGenerator:
    def __init__(self, model: LSTMModel, scaler: MinMaxScaler):
        self.model = model
        self.scaler = scaler
        
    def generate_signals(self, data: np.ndarray, y_test: np.ndarray) -> Tuple[List[int], np.ndarray, np.ndarray]:
        """매매 신호 생성"""
        predictions = self.model.predict(data)
        predictions = self.scaler.inverse_transform(predictions)
        actual = self.scaler.inverse_transform(y_test)
        
        signals = []
        for i in range(len(predictions)-1):
            signals.append(1 if predictions[i+1] > predictions[i] else -1)
            
        return signals, predictions, actual