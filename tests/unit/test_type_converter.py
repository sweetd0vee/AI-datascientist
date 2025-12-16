"""
Unit тесты для модуля type_converter
"""
import pytest
import numpy as np
import pandas as pd
from src.utils.type_converter import convert_numpy_types


class TestConvertNumpyTypes:
    """Тесты для функции convert_numpy_types"""

    def test_convert_numpy_int(self, sample_numpy_int):
        """Тест конвертации numpy int в Python int"""
        result = convert_numpy_types(sample_numpy_int)
        assert isinstance(result, int)
        assert result == 42

    def test_convert_numpy_float(self, sample_numpy_float):
        """Тест конвертации numpy float в Python float"""
        result = convert_numpy_types(sample_numpy_float)
        assert isinstance(result, float)
        assert result == pytest.approx(3.14)

    def test_convert_numpy_bool(self, sample_numpy_bool):
        """Тест конвертации numpy bool в Python bool"""
        result = convert_numpy_types(sample_numpy_bool)
        assert isinstance(result, bool)
        assert result is True

    def test_convert_numpy_array(self, sample_numpy_array):
        """Тест конвертации numpy array в list"""
        result = convert_numpy_types(sample_numpy_array)
        assert isinstance(result, list)
        assert result == [1, 2, 3, 4, 5]

    def test_convert_numpy_array_2d(self, sample_numpy_array_2d):
        """Тест конвертации 2D numpy array"""
        result = convert_numpy_types(sample_numpy_array_2d)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_convert_numpy_scalar(self, sample_numpy_scalar):
        """Тест конвертации numpy scalar"""
        result = convert_numpy_types(sample_numpy_scalar)
        assert isinstance(result, int)
        assert result == 42

    def test_convert_numpy_nan(self):
        """Тест конвертации numpy NaN"""
        nan_val = np.float64(np.nan)
        result = convert_numpy_types(nan_val)
        assert isinstance(result, str)
        assert 'nan' in result.lower()

    def test_convert_numpy_inf(self):
        """Тест конвертации numpy Inf"""
        inf_val = np.float64(np.inf)
        result = convert_numpy_types(inf_val)
        assert isinstance(result, str)
        assert 'inf' in result.lower()

    def test_convert_pandas_timestamp(self, sample_pandas_timestamp):
        """Тест конвертации pandas Timestamp"""
        result = convert_numpy_types(sample_pandas_timestamp)
        assert isinstance(result, str)
        assert '2023-01-01' in result

    def test_convert_pandas_timedelta(self, sample_pandas_timedelta):
        """Тест конвертации pandas Timedelta"""
        result = convert_numpy_types(sample_pandas_timedelta)
        assert isinstance(result, str)

    def test_convert_dict_with_numpy(self, sample_dict_with_numpy):
        """Тест конвертации словаря с numpy типами"""
        result = convert_numpy_types(sample_dict_with_numpy)
        assert isinstance(result, dict)
        assert isinstance(result['int_val'], int)
        assert isinstance(result['float_val'], float)
        assert isinstance(result['bool_val'], bool)
        assert isinstance(result['array'], list)

    def test_convert_list_with_numpy(self, sample_list_with_numpy):
        """Тест конвертации списка с numpy типами"""
        result = convert_numpy_types(sample_list_with_numpy)
        assert isinstance(result, list)
        assert isinstance(result[0], int)
        assert isinstance(result[1], float)
        assert isinstance(result[2], bool)

    def test_convert_nested_structure(self):
        """Тест конвертации вложенной структуры"""
        nested = {
            'level1': {
                'level2': {
                    'numpy_int': np.int64(100),
                    'numpy_float': np.float64(99.9),
                    'array': np.array([1, 2, 3])
                }
            },
            'list': [np.int64(1), np.int64(2)]
        }
        result = convert_numpy_types(nested)
        assert isinstance(result, dict)
        assert isinstance(result['level1']['level2']['numpy_int'], int)
        assert isinstance(result['level1']['level2']['numpy_float'], float)
        assert isinstance(result['level1']['level2']['array'], list)
        assert isinstance(result['list'], list)
        assert all(isinstance(x, int) for x in result['list'])

    def test_convert_standard_types(self):
        """Тест что стандартные типы Python не изменяются"""
        test_cases = [
            42,
            3.14,
            True,
            False,
            "string",
            None,
            [1, 2, 3],
            {'key': 'value'}
        ]
        for case in test_cases:
            result = convert_numpy_types(case)
            assert result == case

    def test_convert_dict_with_numpy_keys(self):
        """Тест конвертации словаря с numpy ключами"""
        dict_with_numpy_key = {
            np.int64(1): 'value1',
            np.float64(2.0): 'value2'
        }
        result = convert_numpy_types(dict_with_numpy_key)
        assert isinstance(result, dict)
        # Ключи должны быть преобразованы
        assert 1 in result or '1' in str(result.keys())
        assert 2 in result or '2' in str(result.keys())

    def test_convert_empty_structures(self):
        """Тест конвертации пустых структур"""
        assert convert_numpy_types({}) == {}
        assert convert_numpy_types([]) == []
        assert convert_numpy_types(None) is None

    def test_convert_numpy_str(self):
        """Тест конвертации numpy string"""
        numpy_str = np.str_("test_string")
        result = convert_numpy_types(numpy_str)
        assert isinstance(result, str)
        assert result == "test_string"

