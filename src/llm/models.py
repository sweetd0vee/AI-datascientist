"""
Инициализация и управление моделями Ollama
"""
import streamlit as st
from langchain_community.llms import Ollama
from config.models_config import MODELS_CONFIG
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@st.cache_resource
def get_llms():
    """
    Инициализация моделей LLM с кэшированием
    
    Returns:
        Tuple[Ollama, Ollama]: Модели для анализа и генерации кода
        
    Raises:
        Exception: Если не удалось подключиться к Ollama
    """
    try:
        analyst_config = MODELS_CONFIG["analyst"]
        coder_config = MODELS_CONFIG["coder"]
        
        llm_analyst = Ollama(
            model=analyst_config["model"],
            temperature=analyst_config["temperature"],
            base_url=analyst_config["base_url"]
        )
        
        llm_coder = Ollama(
            model=coder_config["model"],
            temperature=coder_config["temperature"],
            base_url=coder_config["base_url"]
        )
        
        logger.info("Модели LLM успешно инициализированы")
        return llm_analyst, llm_coder
        
    except Exception as e:
        logger.error(f"Ошибка подключения к Ollama: {e}")
        raise

