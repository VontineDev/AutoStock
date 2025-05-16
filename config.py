# config.py
from dataclasses import dataclass
from typing import Dict, Any
import os
from dotenv import load_dotenv

@dataclass
class Config:
    API_KEY: str
    SYMBOL: str
    SEQUENCE_LENGTH: int = 60
    BATCH_SIZE: int = 32
    EPOCHS: int = 100
    INITIAL_CAPITAL: float = 10000
    TRADING_INTERVAL: int = 3600  # seconds
    
    @classmethod
    def from_env(cls) -> 'Config':
        load_dotenv()
        return cls(
            API_KEY=os.getenv('API_KEY', ''),
            SYMBOL=os.getenv('SYMBOL', 'AAPL'),
            SEQUENCE_LENGTH=int(os.getenv('SEQUENCE_LENGTH', '60')),
            BATCH_SIZE=int(os.getenv('BATCH_SIZE', '32')),
            EPOCHS=int(os.getenv('EPOCHS', '100')),
            INITIAL_CAPITAL=float(os.getenv('INITIAL_CAPITAL', '10000')),
            TRADING_INTERVAL=int(os.getenv('TRADING_INTERVAL', '3600'))
        )