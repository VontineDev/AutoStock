# trading/order_executor.py
import requests
from typing import Dict, Any

class OrderExecutor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def execute_order(self, symbol: str, order_type: str, quantity: int) -> Dict[str, Any]:
        """주문 실행"""
        url = "https://api.broker.com/orders"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "symbol": symbol,
            "order_type": order_type,
            "quantity": quantity
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()