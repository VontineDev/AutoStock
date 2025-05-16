# main.py
from typing import Dict, Any, Optional
import time
from config import Config
from utils.logger import Logger
from data.data_collector import DataCollector
from data.data_processor import DataProcessor
from models.lstm_model import LSTMModel
from trading.signal_generator import SignalGenerator
from trading.order_executor import OrderExecutor
from backtesting.backtest_engine import BacktestEngine

class AutoTradingSystem:
    def __init__(self, config: Config):
        self.config = config
        self.logger = Logger("AutoTradingSystem", "logs/trading.log")
        
        try:
            # 컴포넌트 초기화
            self.data_collector = DataCollector(config.API_KEY)
            self.data_processor = DataProcessor(config.SEQUENCE_LENGTH)
            self.model = LSTMModel(config.SEQUENCE_LENGTH)
            self.signal_generator = SignalGenerator(self.model, self.data_processor.scaler)
            self.order_executor = OrderExecutor(config.API_KEY)
            self.backtest_engine = BacktestEngine(config.INITIAL_CAPITAL)
            
            self.logger.info("Trading system initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize trading system: {str(e)}")
            raise
        
    def run(self) -> None:
        """자동매매 시스템 실행"""
        try:
            # 데이터 수집 및 전처리
            self.logger.info(f"Fetching data for {self.config.SYMBOL}")
            df = self.data_collector.fetch_stock_data(self.config.SYMBOL)
            
            self.logger.info("Preprocessing data")
            x_train, y_train, x_test, y_test, _ = self.data_processor.preprocess_data(df)
            
            # 모델 학습
            self.logger.info("Training model")
            self.model.train(x_train, y_train, 
                           batch_size=self.config.BATCH_SIZE,
                           epochs=self.config.EPOCHS)
            
            # 매매 신호 생성
            self.logger.info("Generating trading signals")
            signals, predictions, actual = self.signal_generator.generate_signals(x_test, y_test)
            
            # 백테스팅
            self.logger.info("Running backtest")
            returns, metrics = self.backtest_engine.run_backtest(signals, actual)
            self.logger.info(f"Backtest returns: {returns:.2f}%")
            self.logger.info(f"Final capital: ${metrics['final_capital']:.2f}")
            
            # 실시간 트레이딩
            self._run_realtime_trading()
            
        except Exception as e:
            self.logger.error(f"Error in trading system: {str(e)}")
            raise
        
    def _run_realtime_trading(self) -> None:
        """실시간 트레이딩 실행"""
        self.logger.info("Starting real-time trading")
        
        while True:
            try:
                current_data = self.data_collector.fetch_realtime_data(self.config.SYMBOL)
                processed_data = self.data_processor.preprocess_realtime_data(current_data)
                prediction = self.model.predict(processed_data)
                
                if prediction[0][0] > current_data['close'].values[-1]:
                    self.logger.info("Generating buy signal")
                    self.order_executor.execute_order(self.config.SYMBOL, "buy", 1)
                else:
                    self.logger.info("Generating sell signal")
                    self.order_executor.execute_order(self.config.SYMBOL, "sell", 1)
                    
                time.sleep(self.config.TRADING_INTERVAL)
                
            except Exception as e:
                self.logger.error(f"Error in real-time trading: {str(e)}")
                time.sleep(60)  # 에러 발생 시 1분 대기 후 재시도

def main() -> None:
    try:
        # 설정 로드
        config = Config.from_env()
        
        # 시스템 실행
        trading_system = AutoTradingSystem(config)
        trading_system.run()
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()