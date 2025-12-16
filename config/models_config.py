"""
Конфигурация моделей LLM
"""
from config.settings import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL_ANALYST,
    OLLAMA_MODEL_CODER,
    OLLAMA_TEMPERATURE_ANALYST,
    OLLAMA_TEMPERATURE_CODER,
)

# Конфигурация моделей
MODELS_CONFIG = {
    "analyst": {
        "model": OLLAMA_MODEL_ANALYST,
        "temperature": OLLAMA_TEMPERATURE_ANALYST,
        "base_url": OLLAMA_BASE_URL,
    },
    "coder": {
        "model": OLLAMA_MODEL_CODER,
        "temperature": OLLAMA_TEMPERATURE_CODER,
        "base_url": OLLAMA_BASE_URL,
    },
}

