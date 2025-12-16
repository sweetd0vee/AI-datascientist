"""
Парсеры ответов от LLM
"""
import re
from typing import Dict, List, Any
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def parse_struct_analyze_response(response_text: str) -> Dict[str, Any]:
    """
    Парсит строковый ответ от LLM по структуре данных.
    
    Args:
        response_text: Текст ответа от LLM
        
    Returns:
        Словарь с распарсенными данными:
        {
            "columns": [{"name": str, "type": str, "description": str}, ...],
            "datetime_candidates": [str, ...]
        }
    """
    logger.debug(f"Попытка парсинга структуры из строки: {repr(response_text[:300])}...")
    
    parsed_data = {"columns": [], "datetime_candidates": []}
    
    # Извлечение блока столбцов
    columns_match = re.search(r"---COLUMNS_START---(.*?)---COLUMNS_END---", response_text, re.DOTALL)
    if columns_match:
        columns_text = columns_match.group(1).strip()
        # Разбиваем на блоки для каждого столбца
        column_blocks = re.split(r'\n\s*\n', columns_text)
        for block in column_blocks:
            if not block.strip():
                continue
            lines = block.strip().split('\n')
            col_info = {}
            for line in lines:
                if line.startswith("Столбец:"):
                    col_info["name"] = line[len("Столбец:"):].strip()
                elif line.startswith("Тип:"):
                    col_info["type"] = line[len("Тип:"):].strip()
                elif line.startswith("Описание:"):
                    col_info["description"] = line[len("Описание:"):].strip()
            if col_info:
                parsed_data["columns"].append(col_info)
    else:
        logger.warning("Не найден блок ---COLUMNS_START---...---COLUMNS_END---")
        return {}
    
    # Извлечение блока datetime кандидатов
    datetime_match = re.search(
        r"---DATETIME_CANDIDATES_START---(.*?)---DATETIME_CANDIDATES_END---", 
        response_text, 
        re.DOTALL
    )
    if datetime_match:
        datetime_text = datetime_match.group(1).strip()
        if datetime_text:
            parsed_data["datetime_candidates"] = [
                name.strip() for name in datetime_text.split(',') if name.strip()
            ]
    
    logger.info("Структура данных успешно распарсена из строки.")
    return parsed_data


def parse_metrics_plan_response(response_text: str) -> Dict[str, List[str]]:
    """
    Парсит строковый ответ от LLM по плану метрик.
    
    Args:
        response_text: Текст ответа от LLM
        
    Returns:
        Словарь {столбец: [список метрик]}
    """
    logger.debug(f"Попытка парсинга плана метрик из строки: {repr(response_text[:300])}...")
    
    parsed_data = {}
    
    # Извлечение блока метрик
    metrics_match = re.search(r"---METRICS_START---(.*?)---METRICS_END---", response_text, re.DOTALL)
    if metrics_match:
        metrics_text = metrics_match.group(1).strip()
        # Разбиваем на блоки для каждого столбца
        column_blocks = re.split(r'\n\s*\n', metrics_text)
        for block in column_blocks:
            if not block.strip():
                continue
            lines = block.strip().split('\n')
            col_name = None
            metrics_list = []
            for line in lines:
                if line.startswith("Столбец:"):
                    col_name = line[len("Столбец:"):].strip()
                elif line.startswith("Метрики:"):
                    metrics_str = line[len("Метрики:"):].strip()
                    metrics_list = [m.strip() for m in metrics_str.split(',') if m.strip()]
            
            if col_name:
                parsed_data[col_name] = metrics_list
    else:
        logger.warning("Не найден блок ---METRICS_START---...---METRICS_END---")
        return {}
    
    logger.info("План метрик успешно распарсен из строки.")
    return parsed_data

