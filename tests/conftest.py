"""
Конфигурация и фикстуры для тестов
"""
import pytest
import numpy as np
import pandas as pd
from datetime import datetime


@pytest.fixture
def sample_numpy_int():
    """Фикстура для numpy integer"""
    return np.int64(42)


@pytest.fixture
def sample_numpy_float():
    """Фикстура для numpy float"""
    return np.float64(3.14)


@pytest.fixture
def sample_numpy_bool():
    """Фикстура для numpy bool"""
    return np.bool_(True)


@pytest.fixture
def sample_numpy_array():
    """Фикстура для numpy array"""
    return np.array([1, 2, 3, 4, 5])


@pytest.fixture
def sample_numpy_array_2d():
    """Фикстура для 2D numpy array"""
    return np.array([[1, 2], [3, 4]])


@pytest.fixture
def sample_numpy_scalar():
    """Фикстура для numpy scalar"""
    return np.array(42)


@pytest.fixture
def sample_pandas_timestamp():
    """Фикстура для pandas Timestamp"""
    return pd.Timestamp('2023-01-01 12:00:00')


@pytest.fixture
def sample_pandas_timedelta():
    """Фикстура для pandas Timedelta"""
    return pd.Timedelta(days=1, hours=2)


@pytest.fixture
def sample_dataframe():
    """Фикстура для pandas DataFrame"""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'score': [85.5, 90.0, 88.5]
    })


@pytest.fixture
def sample_dict_with_numpy():
    """Фикстура для словаря с numpy типами"""
    return {
        'int_val': np.int64(10),
        'float_val': np.float64(3.14),
        'bool_val': np.bool_(True),
        'array': np.array([1, 2, 3])
    }


@pytest.fixture
def sample_list_with_numpy():
    """Фикстура для списка с numpy типами"""
    return [np.int64(1), np.float64(2.5), np.bool_(False)]


@pytest.fixture
def sample_struct_analyze_response():
    """Фикстура для ответа анализа структуры от LLM"""
    return """
---COLUMNS_START---
Столбец: PassengerId
Тип: numerical (integer)
Описание: Уникальный идентификатор пассажира

Столбец: Name
Тип: textual (object)
Описание: Имя пассажира

Столбец: Age
Тип: numerical (float)
Описание: Возраст пассажира
---COLUMNS_END---
---DATETIME_CANDIDATES_START---
SignupDate, LastLoginDate
---DATETIME_CANDIDATES_END---
"""


@pytest.fixture
def sample_metrics_plan_response():
    """Фикстура для ответа плана метрик от LLM"""
    return """
---METRICS_START---
Столбец: Age
Метрики: count, mean, median, mode, std, var, min, max, quantile_25, quantile_75

Столбец: Sex
Метрики: count, nunique, mode, mode_count, mode_rel_freq

Столбец: SignupDate
Метрики: count, min_date, max_date, date_range_days, unique_dates
---METRICS_END---
"""


@pytest.fixture
def sample_invalid_response():
    """Фикстура для невалидного ответа от LLM"""
    return "Это невалидный ответ без нужных блоков"


@pytest.fixture
def sample_empty_response():
    """Фикстура для пустого ответа"""
    return ""

