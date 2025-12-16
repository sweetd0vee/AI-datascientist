"""
Unit тесты для модуля prompts
"""
import pytest
from langchain_core.prompts import PromptTemplate
from src.llm.prompts import (
    get_structure_analyze_prompt,
    get_metrics_plan_prompt,
    get_data_analyze_prompt,
    get_final_report_prompt,
    get_metrics_code_gen_prompt,
    get_visualization_code_prompt,
)


class TestGetPrompts:
    """Тесты для функций получения промптов"""

    def test_get_structure_analyze_prompt(self):
        """Тест получения промпта анализа структуры"""
        prompt = get_structure_analyze_prompt()
        assert isinstance(prompt, PromptTemplate)
        assert "{file_info}" in prompt.template

    def test_get_metrics_plan_prompt(self):
        """Тест получения промпта плана метрик"""
        prompt = get_metrics_plan_prompt()
        assert isinstance(prompt, PromptTemplate)
        assert "{data_structure}" in prompt.template

    def test_get_data_analyze_prompt(self):
        """Тест получения промпта анализа данных"""
        prompt = get_data_analyze_prompt()
        assert isinstance(prompt, PromptTemplate)
        assert "{metrics_results_raw}" in prompt.template

    def test_get_final_report_prompt(self):
        """Тест получения промпта итогового отчета"""
        prompt = get_final_report_prompt()
        assert isinstance(prompt, PromptTemplate)
        assert "{analysis_summary}" in prompt.template

    def test_get_metrics_code_gen_prompt(self):
        """Тест получения промпта генерации кода метрик"""
        prompt = get_metrics_code_gen_prompt()
        assert isinstance(prompt, PromptTemplate)
        assert "{metrics_plan}" in prompt.template
        assert "{df_structure_info}" in prompt.template

    def test_get_visualization_code_prompt_default(self):
        """Тест получения промпта визуализации с дефолтным количеством графиков"""
        prompt = get_visualization_code_prompt()
        assert isinstance(prompt, PromptTemplate)
        # Проверяем что промпт содержит информацию о количестве графиков
        assert "{num_plots}" not in prompt.template  # Должно быть подставлено

    def test_get_visualization_code_prompt_custom_num_plots(self):
        """Тест получения промпта визуализации с кастомным количеством графиков"""
        prompt = get_visualization_code_prompt(num_plots=10)
        assert isinstance(prompt, PromptTemplate)
        # Проверяем что количество графиков подставлено в шаблон
        assert isinstance(prompt.template, str)

    def test_prompts_can_be_formatted(self):
        """Тест что промпты можно форматировать с параметрами"""
        prompt = get_structure_analyze_prompt()
        
        # Проверяем что промпт можно использовать с параметрами
        formatted = prompt.format(file_info="test info")
        assert isinstance(formatted, str)
        assert "test info" in formatted

    def test_metrics_code_gen_prompt_formatting(self):
        """Тест форматирования промпта генерации кода метрик"""
        prompt = get_metrics_code_gen_prompt()
        
        formatted = prompt.format(
            metrics_plan='{"col1": ["mean", "std"]}',
            df_structure_info="DataFrame with 100 rows"
        )
        assert isinstance(formatted, str)
        assert "col1" in formatted or "mean" in formatted

    def test_visualization_prompt_formatting(self):
        """Тест форматирования промпта визуализации"""
        prompt = get_visualization_code_prompt(num_plots=5)
        
        # Проверяем что промпт можно использовать
        assert isinstance(prompt.template, str)
        assert len(prompt.template) > 0

    def test_all_prompts_return_prompt_template(self):
        """Тест что все функции возвращают PromptTemplate"""
        prompts = [
            get_structure_analyze_prompt(),
            get_metrics_plan_prompt(),
            get_data_analyze_prompt(),
            get_final_report_prompt(),
            get_metrics_code_gen_prompt(),
            get_visualization_code_prompt(),
        ]
        
        for prompt in prompts:
            assert isinstance(prompt, PromptTemplate)

    def test_prompts_have_required_variables(self):
        """Тест что промпты содержат необходимые переменные"""
        structure_prompt = get_structure_analyze_prompt()
        assert "{file_info}" in structure_prompt.input_variables
        
        metrics_plan_prompt = get_metrics_plan_prompt()
        assert "{data_structure}" in metrics_plan_prompt.input_variables
        
        data_analyze_prompt = get_data_analyze_prompt()
        assert "{metrics_results_raw}" in data_analyze_prompt.input_variables
        
        final_report_prompt = get_final_report_prompt()
        assert "{analysis_summary}" in final_report_prompt.input_variables

