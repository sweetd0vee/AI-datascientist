"""
Шаблоны промптов для LLM
"""
from langchain_core.prompts import PromptTemplate
from config.prompts_config import (
    STRUCT_ANALYZE_PROMPT,
    METRICS_PLAN_PROMPT,
    DATA_ANALYZE_PROMPT,
    FINAL_REPORT_PROMPT,
    METRICS_CODE_GEN_PROMPT,
    VISUALIZATION_CODE_PROMPT,
)
from config.settings import DEFAULT_NUM_PLOTS


def get_structure_analyze_prompt() -> PromptTemplate:
    """Промпт для анализа структуры данных"""
    return PromptTemplate.from_template(STRUCT_ANALYZE_PROMPT)


def get_metrics_plan_prompt() -> PromptTemplate:
    """Промпт для генерации плана метрик"""
    return PromptTemplate.from_template(METRICS_PLAN_PROMPT)


def get_data_analyze_prompt() -> PromptTemplate:
    """Промпт для анализа метрик"""
    return PromptTemplate.from_template(DATA_ANALYZE_PROMPT)


def get_final_report_prompt() -> PromptTemplate:
    """Промпт для генерации итогового отчета"""
    return PromptTemplate.from_template(FINAL_REPORT_PROMPT)


def get_metrics_code_gen_prompt() -> PromptTemplate:
    """Промпт для генерации кода расчета метрик"""
    return PromptTemplate.from_template(METRICS_CODE_GEN_PROMPT)


def get_visualization_code_prompt(num_plots: int = None) -> PromptTemplate:
    """
    Промпт для генерации кода визуализации
    
    Args:
        num_plots: Количество графиков для генерации
    """
    num_plots = num_plots or DEFAULT_NUM_PLOTS
    prompt_template = VISUALIZATION_CODE_PROMPT.format(num_plots=num_plots)
    return PromptTemplate.from_template(prompt_template)

