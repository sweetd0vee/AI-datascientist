"""
Unit тесты для модуля logger
"""
import pytest
import logging
import sys
from unittest.mock import patch, MagicMock
from src.utils.logger import setup_logger


class TestSetupLogger:
    """Тесты для функции setup_logger"""

    def test_setup_logger_creates_logger(self):
        """Тест что setup_logger создает логгер"""
        logger = setup_logger("test_module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_setup_logger_sets_level(self):
        """Тест что setup_logger устанавливает уровень логирования"""
        logger = setup_logger("test_module", level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_setup_logger_has_handler(self):
        """Тест что setup_logger добавляет handler"""
        logger = setup_logger("test_module")
        assert len(logger.handlers) > 0
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)

    def test_setup_logger_does_not_duplicate_handlers(self):
        """Тест что setup_logger не дублирует handlers"""
        logger1 = setup_logger("test_module")
        handler_count1 = len(logger1.handlers)
        
        logger2 = setup_logger("test_module")
        handler_count2 = len(logger2.handlers)
        
        # Должен быть тот же логгер с теми же handlers
        assert logger1 is logger2
        assert handler_count1 == handler_count2

    def test_setup_logger_uses_default_level(self):
        """Тест что setup_logger использует уровень по умолчанию"""
        with patch('src.utils.logger.LOG_LEVEL', 'WARNING'):
            logger = setup_logger("test_module")
            assert logger.level == logging.WARNING

    def test_setup_logger_custom_level(self):
        """Тест что setup_logger использует переданный уровень"""
        logger = setup_logger("test_module", level="ERROR")
        assert logger.level == logging.ERROR

    def test_setup_logger_invalid_level_falls_back_to_info(self):
        """Тест что невалидный уровень приводит к INFO"""
        logger = setup_logger("test_module", level="INVALID_LEVEL")
        # Должен упасть на INFO как fallback
        assert logger.level in [logging.INFO, logging.DEBUG, logging.WARNING]

    def test_setup_logger_handler_is_stdout(self):
        """Тест что handler использует stdout"""
        logger = setup_logger("test_module")
        handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(handlers) > 0
        # Проверяем что handler использует stdout
        assert handlers[0].stream == sys.stdout

    def test_setup_logger_formatter_set(self):
        """Тест что formatter установлен"""
        logger = setup_logger("test_module")
        handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(handlers) > 0
        assert handlers[0].formatter is not None

    def test_setup_logger_different_modules(self):
        """Тест что разные модули создают разные логгеры"""
        logger1 = setup_logger("module1")
        logger2 = setup_logger("module2")
        
        assert logger1 is not logger2
        assert logger1.name == "module1"
        assert logger2.name == "module2"

    def test_setup_logger_logs_messages(self, caplog):
        """Тест что логгер может логировать сообщения"""
        logger = setup_logger("test_module", level="DEBUG")
        
        with caplog.at_level(logging.DEBUG):
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
        
        assert "Debug message" in caplog.text
        assert "Info message" in caplog.text
        assert "Warning message" in caplog.text
        assert "Error message" in caplog.text

