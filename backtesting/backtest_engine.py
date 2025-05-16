# backtesting/backtest_engine.py
from typing import List, Tuple
import numpy as np

class BacktestEngine:
    def __init__(self, initial_capital: float = 10000):
        self.initial_capital = initial_capital
        
    def run_backtest(self, signals: List[int], actual_prices: np.ndarray) -> Tuple[float, Dict[str, float]]:
        """백테스팅 실행"""
        capital = self.initial_capital
        shares = 0
        
        for i in range(len(signals)):
            if signals[i] == 1:  # 매수
                shares_to_buy = capital // actual_prices[i]
                shares += shares_to_buy
                capital -= shares_to_buy * actual_prices[i]
            elif signals[i] == -1 and shares > 0:  # 매도
                capital += shares * actual_prices[i]
                shares = 0
                
        final_capital = capital + shares * actual_prices[-1]
        returns = (final_capital - self.initial_capital) / self.initial_capital * 100
        
        return returns, {
            'final_capital': final_capital,
            'total_trades': len(signals),
            'shares_held': shares
        }