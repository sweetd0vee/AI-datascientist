"""
Unit тесты для модуля parsers
"""
import pytest
from src.llm.parsers import parse_struct_analyze_response, parse_metrics_plan_response


class TestParseStructAnalyzeResponse:
    """Тесты для функции parse_struct_analyze_response"""

    def test_parse_valid_response(self, sample_struct_analyze_response):
        """Тест парсинга валидного ответа"""
        result = parse_struct_analyze_response(sample_struct_analyze_response)
        
        assert isinstance(result, dict)
        assert "columns" in result
        assert "datetime_candidates" in result
        assert len(result["columns"]) == 3
        
        # Проверка первого столбца
        assert result["columns"][0]["name"] == "PassengerId"
        assert result["columns"][0]["type"] == "numerical (integer)"
        assert result["columns"][0]["description"] == "Уникальный идентификатор пассажира"
        
        # Проверка datetime кандидатов
        assert len(result["datetime_candidates"]) == 2
        assert "SignupDate" in result["datetime_candidates"]
        assert "LastLoginDate" in result["datetime_candidates"]

    def test_parse_response_without_datetime_candidates(self):
        """Тест парсинга ответа без datetime кандидатов"""
        response = """
---COLUMNS_START---
Столбец: Age
Тип: numerical (float)
Описание: Возраст
---COLUMNS_END---
---DATETIME_CANDIDATES_START---

---DATETIME_CANDIDATES_END---
"""
        result = parse_struct_analyze_response(response)
        
        assert isinstance(result, dict)
        assert len(result["columns"]) == 1
        assert len(result["datetime_candidates"]) == 0

    def test_parse_response_with_empty_datetime_block(self):
        """Тест парсинга ответа с пустым блоком datetime"""
        response = """
---COLUMNS_START---
Столбец: Name
Тип: textual
Описание: Имя
---COLUMNS_END---
---DATETIME_CANDIDATES_START---
---DATETIME_CANDIDATES_END---
"""
        result = parse_struct_analyze_response(response)
        
        assert len(result["datetime_candidates"]) == 0

    def test_parse_invalid_response(self, sample_invalid_response):
        """Тест парсинга невалидного ответа"""
        result = parse_struct_analyze_response(sample_invalid_response)
        
        assert result == {}

    def test_parse_empty_response(self, sample_empty_response):
        """Тест парсинга пустого ответа"""
        result = parse_struct_analyze_response(sample_empty_response)
        
        assert result == {}

    def test_parse_response_with_multiple_columns(self):
        """Тест парсинга ответа с несколькими столбцами"""
        response = """
---COLUMNS_START---
Столбец: Col1
Тип: type1
Описание: Description1

Столбец: Col2
Тип: type2
Описание: Description2

Столбец: Col3
Тип: type3
Описание: Description3
---COLUMNS_END---
---DATETIME_CANDIDATES_START---
Col1
---DATETIME_CANDIDATES_END---
"""
        result = parse_struct_analyze_response(response)
        
        assert len(result["columns"]) == 3
        assert result["columns"][0]["name"] == "Col1"
        assert result["columns"][1]["name"] == "Col2"
        assert result["columns"][2]["name"] == "Col3"

    def test_parse_response_with_whitespace(self):
        """Тест парсинга ответа с лишними пробелами"""
        response = """
---COLUMNS_START---
Столбец:   Col1   
Тип:   type1   
Описание:   Description1   
---COLUMNS_END---
---DATETIME_CANDIDATES_START---
  Col1  ,  Col2  
---DATETIME_CANDIDATES_END---
"""
        result = parse_struct_analyze_response(response)
        
        assert result["columns"][0]["name"] == "Col1"
        assert result["columns"][0]["type"] == "type1"
        assert len(result["datetime_candidates"]) == 2
        assert result["datetime_candidates"][0] == "Col1"
        assert result["datetime_candidates"][1] == "Col2"

    def test_parse_response_missing_description(self):
        """Тест парсинга ответа без описания"""
        response = """
---COLUMNS_START---
Столбец: Col1
Тип: type1
---COLUMNS_END---
---DATETIME_CANDIDATES_START---
---DATETIME_CANDIDATES_END---
"""
        result = parse_struct_analyze_response(response)
        
        assert len(result["columns"]) == 1
        assert "name" in result["columns"][0]
        assert "type" in result["columns"][0]
        # Описание может отсутствовать
        assert "description" not in result["columns"][0] or result["columns"][0]["description"] == ""


class TestParseMetricsPlanResponse:
    """Тесты для функции parse_metrics_plan_response"""

    def test_parse_valid_response(self, sample_metrics_plan_response):
        """Тест парсинга валидного ответа плана метрик"""
        result = parse_metrics_plan_response(sample_metrics_plan_response)
        
        assert isinstance(result, dict)
        assert len(result) == 3
        
        # Проверка метрик для Age
        assert "Age" in result
        assert isinstance(result["Age"], list)
        assert "count" in result["Age"]
        assert "mean" in result["Age"]
        assert "median" in result["Age"]
        
        # Проверка метрик для Sex
        assert "Sex" in result
        assert "nunique" in result["Sex"]
        assert "mode" in result["Sex"]
        
        # Проверка метрик для SignupDate
        assert "SignupDate" in result
        assert "min_date" in result["SignupDate"]
        assert "max_date" in result["SignupDate"]

    def test_parse_invalid_response(self, sample_invalid_response):
        """Тест парсинга невалидного ответа"""
        result = parse_metrics_plan_response(sample_invalid_response)
        
        assert result == {}

    def test_parse_empty_response(self, sample_empty_response):
        """Тест парсинга пустого ответа"""
        result = parse_metrics_plan_response(sample_empty_response)
        
        assert result == {}

    def test_parse_response_with_multiple_metrics(self):
        """Тест парсинга ответа с множеством метрик"""
        response = """
---METRICS_START---
Столбец: Col1
Метрики: metric1, metric2, metric3, metric4, metric5

Столбец: Col2
Метрики: metricA, metricB
---METRICS_END---
"""
        result = parse_metrics_plan_response(response)
        
        assert len(result) == 2
        assert len(result["Col1"]) == 5
        assert len(result["Col2"]) == 2
        assert result["Col1"] == ["metric1", "metric2", "metric3", "metric4", "metric5"]
        assert result["Col2"] == ["metricA", "metricB"]

    def test_parse_response_with_whitespace_in_metrics(self):
        """Тест парсинга ответа с пробелами в метриках"""
        response = """
---METRICS_START---
Столбец: Col1
Метрики:  metric1  ,  metric2  ,  metric3  
---METRICS_END---
"""
        result = parse_metrics_plan_response(response)
        
        assert len(result["Col1"]) == 3
        assert result["Col1"] == ["metric1", "metric2", "metric3"]

    def test_parse_response_with_empty_metrics(self):
        """Тест парсинга ответа с пустым списком метрик"""
        response = """
---METRICS_START---
Столбец: Col1
Метрики: 
---METRICS_END---
"""
        result = parse_metrics_plan_response(response)
        
        assert "Col1" in result
        assert result["Col1"] == []

    def test_parse_response_with_single_metric(self):
        """Тест парсинга ответа с одной метрикой"""
        response = """
---METRICS_START---
Столбец: Col1
Метрики: single_metric
---METRICS_END---
"""
        result = parse_metrics_plan_response(response)
        
        assert result["Col1"] == ["single_metric"]

    def test_parse_response_with_special_characters(self):
        """Тест парсинга ответа со специальными символами в названиях"""
        response = """
---METRICS_START---
Столбец: Col-Name_1
Метрики: metric-name_1, metric.name_2
---METRICS_END---
"""
        result = parse_metrics_plan_response(response)
        
        assert "Col-Name_1" in result
        assert "metric-name_1" in result["Col-Name_1"]
        assert "metric.name_2" in result["Col-Name_1"]

