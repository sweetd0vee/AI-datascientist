"""
Настройка системы логирования
"""
import logging
import sys
from config.settings import LOG_LEVEL, LOG_FORMAT


def setup_logger(name: str = __name__, level: str = None) -> logging.Logger:
    """
    Настройка логгера для модуля
    
    Args:
        name: Имя логгера (обычно __name__)
        level: Уровень логирования (если None, используется из настроек)
    
    Returns:
        Настроенный логгер
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
    
    log_level = level or LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    return logger

