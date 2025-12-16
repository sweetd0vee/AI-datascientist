# Руководство по миграции кода

Это руководство поможет перенести существующий код из `ins_temp3.py` в новую модульную архитектуру.

## Общий план миграции

### Этап 1: Подготовка
- ✅ Создана структура директорий
- ✅ Созданы базовые модули и конфигурация
- ⏳ Рефакторинг существующего кода

### Этап 2: Рефакторинг по модулям

#### 2.1. Utils модуль
**Файл**: `src/utils/code_executor.py`
- Перенести функции:
  - `extract_python_code()` → `code_executor.py`
  - `safe_code_execution()` → `code_executor.py`
  - `static_code_analysis()` → `code_executor.py`
- Уже перенесено:
  - `convert_numpy_types()` → `type_converter.py` ✅
  - Настройка логирования → `logger.py` ✅

#### 2.2. Data модуль
**Файл**: `src/data/loader.py`
- Перенести функции:
  - `load_df_from_state()` → `loader.py`
  - Логика загрузки CSV/Excel → `loader.py`

**Файл**: `src/data/preprocessor.py`
- Перенести функции:
  - `preprocess_dates_based_on_llm()` → `preprocessor.py`
  - `handle_missing_values_before_analysis()` → `preprocessor.py`
  - `get_df_info()` → `preprocessor.py`

#### 2.3. LLM модуль
- Уже создано:
  - `models.py` - инициализация моделей ✅
  - `prompts.py` - шаблоны промптов ✅
  - `parsers.py` - парсинг ответов ✅

**Файл**: `src/llm/chains.py` (создать)
- Перенести создание цепочек LangChain:
  - `chain_structure` → `create_structure_chain()`
  - `chain_metrics_plan` → `create_metrics_plan_chain()`
  - `chain_code_gen` → `create_code_gen_chain()`
  - `chain_analysis` → `create_analysis_chain()`
  - `chain_viz_code` → `create_viz_chain()`
  - `chain_report` → `create_report_chain()`

#### 2.4. Core модуль
**Файл**: `src/core/orchestrator.py` (создать)
- Создать класс `AnalysisOrchestrator`:
  ```python
  class AnalysisOrchestrator:
      def __init__(self, llm_analyst, llm_coder, ...):
          ...
      
      def run_analysis(self, df, output_dir):
          # Весь процесс анализа из ins_temp3.py
          ...
  ```

**Файл**: `src/core/pipeline.py` (создать)
- Создать класс `AnalysisPipeline`:
  ```python
  class AnalysisPipeline:
      def __init__(self):
          self.steps = []
      
      def add_step(self, step):
          ...
      
      def execute(self, data):
          ...
  ```

#### 2.5. UI модуль
**Файл**: `src/ui/main.py` (создать)
- Перенести Streamlit код:
  - Настройка страницы
  - Загрузка файлов
  - Отображение результатов
  - Интеграция с `AnalysisOrchestrator`

**Файл**: `src/ui/components/file_upload.py` (создать)
- Компонент загрузки файлов

**Файл**: `src/ui/components/results_view.py` (создать)
- Компонент отображения результатов

### Этап 3: Интеграция

1. Обновить импорты в `src/ui/main.py`
2. Создать точку входа `main.py` в корне проекта (опционально)
3. Обновить `requirements.txt` при необходимости

## Детальный план переноса функций

### Функции из ins_temp3.py → Новые модули

| Функция | Текущее место | Новое место | Статус |
|---------|---------------|-------------|--------|
| `extract_python_code()` | ins_temp3.py:196 | `src/utils/code_executor.py` | ⏳ |
| `convert_numpy_types()` | ins_temp3.py:218 | `src/utils/type_converter.py` | ✅ |
| `parse_struct_analyze_response()` | ins_temp3.py:275 | `src/llm/parsers.py` | ✅ |
| `parse_metrics_plan_response()` | ins_temp3.py:324 | `src/llm/parsers.py` | ✅ |
| `static_code_analysis()` | ins_temp3.py:365 | `src/utils/code_executor.py` | ⏳ |
| `load_df_from_state()` | ins_temp3.py:399 | `src/data/loader.py` | ⏳ |
| `preprocess_dates_based_on_llm()` | ins_temp3.py:448 | `src/data/preprocessor.py` | ⏳ |
| `handle_missing_values_before_analysis()` | ins_temp3.py:497 | `src/data/preprocessor.py` | ⏳ |
| `safe_code_execution()` | ins_temp3.py:559 | `src/utils/code_executor.py` | ⏳ |
| `get_df_info()` | ins_temp3.py:645 | `src/data/preprocessor.py` | ⏳ |

### Промпты → config/prompts_config.py

| Промпт | Статус |
|--------|--------|
| `struct_analyze` | ✅ |
| `m_plan` | ✅ |
| `data_analyze` | ✅ |
| `final_rep` | ✅ |
| Промпт генерации кода метрик | ✅ |
| Промпт генерации визуализации | ✅ |

### Настройки → config/settings.py

| Настройка | Статус |
|-----------|--------|
| Пути и директории | ✅ |
| Настройки LLM | ✅ |
| Настройки логирования | ✅ |
| Настройки файлов | ✅ |

## Примеры миграции

### Пример 1: Перенос функции загрузки данных

**Было** (ins_temp3.py):
```python
def load_df_from_state():
    """Загружает df из st.session_state..."""
    ...
```

**Станет** (src/data/loader.py):
```python
from typing import Optional
import pandas as pd
import streamlit as st

def load_dataframe(file_path: Optional[str] = None, uploaded_file=None) -> Optional[pd.DataFrame]:
    """
    Загружает DataFrame из файла или загруженного файла.
    
    Args:
        file_path: Путь к файлу
        uploaded_file: Загруженный файл через Streamlit
        
    Returns:
        DataFrame или None при ошибке
    """
    ...
```

### Пример 2: Создание оркестратора

**Было** (ins_temp3.py):
```python
# Весь код анализа в одном месте
if st.button("🚀 Запустить анализ"):
    # Шаг 1: Анализ структуры
    # Шаг 2: План метрик
    # ...
```

**Станет** (src/core/orchestrator.py):
```python
class AnalysisOrchestrator:
    def __init__(self, llm_analyst, llm_coder, ...):
        self.llm_analyst = llm_analyst
        self.llm_coder = llm_coder
        ...
    
    def run_analysis(self, df, output_dir):
        # Шаг 1: Анализ структуры
        structure = self.analyze_structure(df)
        
        # Шаг 2: План метрик
        metrics_plan = self.generate_metrics_plan(structure)
        
        # ...
        
        return results
```

## Проверка после миграции

1. ✅ Все импорты корректны
2. ✅ Все функции перенесены
3. ✅ Конфигурация вынесена в отдельные файлы
4. ✅ Код разделен на модули
5. ✅ Тесты проходят (когда будут добавлены)
6. ✅ Приложение запускается и работает

## Следующие шаги

1. Постепенно переносить функции из `ins_temp3.py` в соответствующие модули
2. Тестировать каждый модуль после переноса
3. Обновлять документацию
4. Добавлять тесты для новых модулей
5. После полной миграции можно удалить `ins_temp3.py` или оставить как reference

