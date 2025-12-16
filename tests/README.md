# Тесты проекта AI Data Scientist

## Структура тестов

```
tests/
├── conftest.py              # Конфигурация и фикстуры
├── unit/                    # Unit тесты
│   ├── test_type_converter.py
│   ├── test_logger.py
│   ├── test_parsers.py
│   └── test_prompts.py
├── integration/            # Интеграционные тесты
└── fixtures/               # Тестовые данные
```

## Запуск тестов

### Все тесты
```bash
pytest
```

### Только unit тесты
```bash
pytest tests/unit/
```

### С покрытием кода
```bash
pytest --cov=src --cov-report=html
```

### Конкретный тест
```bash
pytest tests/unit/test_type_converter.py::TestConvertNumpyTypes::test_convert_numpy_int
```

### С маркерами
```bash
# Только unit тесты
pytest -m unit

# Исключить медленные тесты
pytest -m "not slow"
```

## Покрытие кода

Текущее минимальное покрытие: 70%

Просмотр отчета о покрытии:
```bash
pytest --cov=src --cov-report=html
# Откройте htmlcov/index.html в браузере
```

## Написание новых тестов

### Структура теста

```python
import pytest
from src.module.function import function_to_test

class TestFunctionToTest:
    """Описание класса тестов"""
    
    def test_something(self):
        """Описание теста"""
        # Arrange
        input_data = ...
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == expected_value
```

### Использование фикстур

Фикстуры определены в `conftest.py`:

```python
def test_with_fixture(sample_numpy_int):
    result = convert_numpy_types(sample_numpy_int)
    assert isinstance(result, int)
```

### Маркеры

- `@pytest.mark.unit` - Unit тесты
- `@pytest.mark.integration` - Интеграционные тесты
- `@pytest.mark.slow` - Медленные тесты
- `@pytest.mark.llm` - Тесты требующие LLM

## Best Practices

1. **Именование**: `test_<function_name>_<scenario>`
2. **Один тест - одна проверка**: Каждый тест проверяет одну вещь
3. **AAA паттерн**: Arrange, Act, Assert
4. **Использование фикстур**: Для переиспользуемых данных
5. **Изоляция**: Тесты не должны зависеть друг от друга
6. **Читаемость**: Тесты должны быть понятными без комментариев

## Примеры

### Тест функции конвертации типов
```python
def test_convert_numpy_int(sample_numpy_int):
    result = convert_numpy_types(sample_numpy_int)
    assert isinstance(result, int)
    assert result == 42
```

### Тест парсера с моком
```python
def test_parse_response(mocker):
    mock_logger = mocker.patch('src.llm.parsers.logger')
    result = parse_struct_analyze_response("test")
    assert result == {}
    mock_logger.warning.assert_called_once()
```

## CI/CD

Тесты автоматически запускаются в CI/CD пайплайне. Убедитесь что все тесты проходят перед коммитом:

```bash
pytest --cov=src --cov-fail-under=70
```

