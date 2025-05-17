# utils/logger.py
import logging
import os
from typing import Optional

class Logger:
    def __init__(self, name: str, log_file: Optional[str] = None, level: int = logging.INFO):
        # 로그 디렉토리 생성
        if log_file:
            log_dir = os.path.dirname(log_file)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
        
        # 로거 설정
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 핸들러가 중복으로 추가되지 않도록 기존 핸들러 제거
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        
        # 콘솔 핸들러 추가
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # 파일 핸들러 추가 (선택적)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str) -> None:
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        self.logger.debug(message)