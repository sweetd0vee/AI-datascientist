"""
Unit тесты для модулей конфигурации
"""
import pytest
import os
from unittest.mock import patch


class TestSettings:
    """Тесты для config.settings"""

    def test_settings_imports(self):
        """Тест что настройки можно импортировать"""
        from config.settings import (
            BASE_DIR,
            OLLAMA_BASE_URL,
            OLLAMA_MODEL_ANALYST,
            OLLAMA_MODEL_CODER,
            LOG_LEVEL,
            DEFAULT_OUTPUT_DIR,
        )
        
        assert BASE_DIR is not None
        assert isinstance(OLLAMA_BASE_URL, str)
        assert isinstance(OLLAMA_MODEL_ANALYST, str)
        assert isinstance(OLLAMA_MODEL_CODER, str)
        assert isinstance(LOG_LEVEL, str)
        assert isinstance(DEFAULT_OUTPUT_DIR, str)

    @patch.dict(os.environ, {'OLLAMA_BASE_URL': 'http://test:11434'})
    def test_settings_uses_env_vars(self):
        """Тест что настройки используют переменные окружения"""
        # Перезагружаем модуль для применения переменных окружения
        import importlib
        import config.settings
        importlib.reload(config.settings)
        
        assert config.settings.OLLAMA_BASE_URL == 'http://test:11434'


class TestPromptsConfig:
    """Тесты для config.prompts_config"""

    def test_prompts_config_imports(self):
        """Тест что промпты можно импортировать"""
        from config.prompts_config import (
            STRUCT_ANALYZE_PROMPT,
            METRICS_PLAN_PROMPT,
            DATA_ANALYZE_PROMPT,
            FINAL_REPORT_PROMPT,
            METRICS_CODE_GEN_PROMPT,
            VISUALIZATION_CODE_PROMPT,
        )
        
        assert isinstance(STRUCT_ANALYZE_PROMPT, str)
        assert isinstance(METRICS_PLAN_PROMPT, str)
        assert isinstance(DATA_ANALYZE_PROMPT, str)
        assert isinstance(FINAL_REPORT_PROMPT, str)
        assert isinstance(METRICS_CODE_GEN_PROMPT, str)
        assert isinstance(VISUALIZATION_CODE_PROMPT, str)

    def test_prompts_contain_placeholders(self):
        """Тест что промпты содержат необходимые плейсхолдеры"""
        from config.prompts_config import (
            STRUCT_ANALYZE_PROMPT,
            METRICS_PLAN_PROMPT,
            DATA_ANALYZE_PROMPT,
            FINAL_REPORT_PROMPT,
        )
        
        assert "{file_info}" in STRUCT_ANALYZE_PROMPT
        assert "{data_structure}" in METRICS_PLAN_PROMPT
        assert "{metrics_results_raw}" in DATA_ANALYZE_PROMPT
        assert "{analysis_summary}" in FINAL_REPORT_PROMPT


class TestModelsConfig:
    """Тесты для config.models_config"""

    def test_models_config_imports(self):
        """Тест что конфигурация моделей можно импортировать"""
        from config.models_config import MODELS_CONFIG
        
        assert isinstance(MODELS_CONFIG, dict)
        assert "analyst" in MODELS_CONFIG
        assert "coder" in MODELS_CONFIG

    def test_models_config_structure(self):
        """Тест структуры конфигурации моделей"""
        from config.models_config import MODELS_CONFIG
        
        analyst_config = MODELS_CONFIG["analyst"]
        coder_config = MODELS_CONFIG["coder"]
        
        assert "model" in analyst_config
        assert "temperature" in analyst_config
        assert "base_url" in analyst_config
        
        assert "model" in coder_config
        assert "temperature" in coder_config
        assert "base_url" in coder_config

