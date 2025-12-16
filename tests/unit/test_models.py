"""
Unit тесты для модуля models (с моками)
"""
import pytest
from unittest.mock import patch, MagicMock
from langchain_community.llms import Ollama


class TestGetLLMs:
    """Тесты для функции get_llms"""

    @patch('src.llm.models.Ollama')
    @patch('src.llm.models.MODELS_CONFIG')
    def test_get_llms_initializes_models(self, mock_config, mock_ollama):
        """Тест что get_llms инициализирует модели"""
        # Настройка моков
        mock_config.__getitem__.side_effect = lambda key: {
            "analyst": {"model": "analyst-model", "temperature": 0.5, "base_url": "http://localhost"},
            "coder": {"model": "coder-model", "temperature": 0.2, "base_url": "http://localhost"}
        }[key]
        
        mock_llm_instance = MagicMock()
        mock_ollama.return_value = mock_llm_instance
        
        # Импорт и вызов функции
        from src.llm.models import get_llms
        
        # Вызов функции (в реальности это будет через @st.cache_resource)
        llm_analyst, llm_coder = get_llms()
        
        # Проверки
        assert llm_analyst is not None
        assert llm_coder is not None
        assert mock_ollama.call_count == 2

    @patch('src.llm.models.Ollama')
    def test_get_llms_handles_exception(self, mock_ollama):
        """Тест обработки исключений при инициализации"""
        mock_ollama.side_effect = Exception("Connection error")
        
        from src.llm.models import get_llms
        
        with pytest.raises(Exception):
            get_llms()

