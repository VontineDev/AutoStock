# backtesting/backtest_engine.py
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Any

class BacktestEngine:
    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        
    def run_backtest(self, signals: List[int], prices: np.ndarray) -> Tuple[float, Dict[str, Any]]:
        """백테스트 실행"""
        capital = self.initial_capital
        position = 0  # 보유 주식 수
        trades = []
        
        for i in range(len(signals)):
            current_price = prices[i][0]
            signal = signals[i]
            
            if signal == 1 and position == 0:  # 매수 신호 & 미보유 상태
                # 가용 자금의 90%로 매수
                shares_to_buy = int((capital * 0.9) / current_price)
                if shares_to_buy > 0:
                    cost = shares_to_buy * current_price
                    capital -= cost
                    position += shares_to_buy
                    trades.append({
                        "type": "buy",
                        "price": current_price,
                        "shares": shares_to_buy,
                        "cost": cost
                    })
            
            elif signal == -1 and position > 0:  # 매도 신호 & 보유 상태
                # 모든 주식 매도
                proceeds = position * current_price
                capital += proceeds
                trades.append({
                    "type": "sell",
                    "price": current_price,
                    "shares": position,
                    "proceeds": proceeds
                })
                position = 0
        
        # 마지막에 남은 포지션 정리
        if position > 0:
            final_price = prices[-1][0]
            proceeds = position * final_price
            capital += proceeds
            trades.append({
                "type": "sell",
                "price": final_price,
                "shares": position,
                "proceeds": proceeds
            })
        
        # 성과 지표 계산
        final_capital = capital
        returns = ((final_capital - self.initial_capital) / self.initial_capital) * 100
        
        # 승률 계산
        winning_trades = 0
        for i in range(len(trades)):
            if trades[i]["type"] == "sell" and i > 0 and trades[i-1]["type"] == "buy":
                if trades[i]["price"] > trades[i-1]["price"]:
                    winning_trades += 1
        
        win_rate = (winning_trades / (len(trades) // 2)) * 100 if len(trades) > 0 else 0
        
        metrics = {
            "final_capital": final_capital,
            "trades": len(trades),
            "win_rate": win_rate,
            "start_date": pd.to_datetime(prices[0][0]).strftime('%Y-%m-%d') if len(prices) > 0 else None,
            "end_date": pd.to_datetime(prices[-1][0]).strftime('%Y-%m-%d') if len(prices) > 0 else None
        }
        
        return returns, metrics