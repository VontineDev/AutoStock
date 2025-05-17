# data/data_collector.py
import requests
import pandas as pd
import datetime
from typing import Dict, Any

class DataCollector:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://finnhub.io/api/v1"
        
    def fetch_stock_data(self, symbol: str) -> pd.DataFrame:
        """Finnhub API를 통해 주식 데이터 가져오기"""
        # 현재 시간 및 2년 전 시간 (Unix 타임스탬프)
        end_time = int(datetime.datetime.now().timestamp())
        start_time = int((datetime.datetime.now() - datetime.timedelta(days=730)).timestamp())
        
        url = f"{self.base_url}/stock/candle?symbol={symbol}&resolution=D&from={start_time}&to={end_time}&token={self.api_key}"
        response = requests.get(url)
        data = response.json()
        
        if data.get('s') == 'ok':
            df = pd.DataFrame({
                'timestamp': data['t'],
                'open': data['o'],
                'high': data['h'],
                'low': data['l'],
                'close': data['c'],
                'volume': data['v']
            })
            
            # 타임스탬프를 날짜로 변환
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('timestamp', inplace=True)
            
            return df.sort_index()
        else:
            raise Exception(f"API 오류: {data.get('s')}")
    
    def fetch_realtime_data(self, symbol: str, limit: int = 60) -> pd.DataFrame:
        """Finnhub API를 통해 실시간 데이터 가져오기 (실제로는 최근 인트라데이 데이터)"""
        # 현재 시간 및 1일 전 시간 (Unix 타임스탬프)
        end_time = int(datetime.datetime.now().timestamp())
        start_time = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp())
        
        # 5분 캔들 데이터 요청
        url = f"{self.base_url}/stock/candle?symbol={symbol}&resolution=5&from={start_time}&to={end_time}&token={self.api_key}"
        response = requests.get(url)
        data = response.json()
        
        if data.get('s') == 'ok':
            df = pd.DataFrame({
                'timestamp': data['t'],
                'open': data['o'],
                'high': data['h'],
                'low': data['l'],
                'close': data['c'],
                'volume': data['v']
            })
            
            # 타임스탬프를 날짜로 변환
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('timestamp', inplace=True)
            
            # 최근 'limit'개 데이터만 반환
            return df.sort_index().tail(limit)
        else:
            raise Exception(f"API 오류: {data.get('s')}")
            
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """회사 프로필 정보 가져오기"""
        url = f"{self.base_url}/stock/profile2?symbol={symbol}&token={self.api_key}"
        response = requests.get(url)
        return response.json()