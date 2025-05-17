# trading/signal_generator.py
import numpy as np
from typing import Tuple, List
from sklearn.preprocessing import MinMaxScaler
from models.lstm_model import LSTMModel

class SignalGenerator:
    def __init__(self, model: LSTMModel, scaler: MinMaxScaler, threshold: float = 0.01):
        self.model = model
        self.scaler = scaler
        self.threshold = threshold  # 매수/매도 신호 생성을 위한 임계값
        
    def generate_signals(self, x_test: np.ndarray, y_test: np.ndarray) -> Tuple[List[int], np.ndarray, np.ndarray]:
        """테스트 데이터에 대한 매매 신호 생성"""
        # 예측값 계산
        predictions = self.model.predict(x_test)
        
        # 원래 스케일로 변환
        predictions_original = self.scaler.inverse_transform(predictions)
        y_test_original = self.scaler.inverse_transform(y_test)
        
        # 매매 신호 생성 (1: 매수, -1: 매도, 0: 홀드)
        signals = []
        
        for i in range(len(predictions_original)):
            # 현재 종가
            current_price = self.scaler.inverse_transform(x_test[i][-1].reshape(-1, 1))[0][0]
            # 예측 종가
            predicted_price = predictions_original[i][0]
            
            # 가격 변화율
            change_percent = (predicted_price - current_price) / current_price
            
            if change_percent > self.threshold:
                signals.append(1)  # 매수 신호
            elif change_percent < -self.threshold:
                signals.append(-1)  # 매도 신호
            else:
                signals.append(0)  # 홀드 신호
        
        return signals, predictions_original, y_test_original