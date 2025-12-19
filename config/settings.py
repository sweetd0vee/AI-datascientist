"""
Основные настройки приложения
"""
import os
from pathlib import Path
from typing import Optional

# Базовые пути
BASE_DIR = Path(__file__).parent.parent
PROJECT_ROOT = BASE_DIR

# Настройки LLM
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL_ANALYST = os.getenv("OLLAMA_MODEL_ANALYST", "llama2:latest")
OLLAMA_MODEL_CODER = os.getenv("OLLAMA_MODEL_CODER", "qwen3-coder:latest")
OLLAMA_TEMPERATURE_ANALYST = float(os.getenv("OLLAMA_TEMPERATURE_ANALYST", "0.55"))
OLLAMA_TEMPERATURE_CODER = float(os.getenv("OLLAMA_TEMPERATURE_CODER", "0.2"))

# Настройки логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Настройки выходных данных
DEFAULT_OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./outputs")
OUTPUT_DIR = Path(DEFAULT_OUTPUT_DIR)

# Поддерживаемые форматы файлов
SUPPORTED_FILE_FORMATS = [".csv", ".xlsx", ".xls"]
MAX_FILE_SIZE_MB = 100

# Настройки Streamlit
STREAMLIT_PAGE_TITLE = "Анализ данных с LangChain"
STREAMLIT_PAGE_LAYOUT = "wide"

# Настройки выполнения кода
CODE_EXECUTION_TIMEOUT = 300  # секунды
ALLOWED_IMPORTS = ["pandas", "numpy", "matplotlib", "seaborn", "scipy"]

# Настройки визуализации
DEFAULT_NUM_PLOTS = 30
PLOT_FORMAT = "png"
PLOT_DPI = 100
