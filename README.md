# AI Data Scientist

Автоматизированная система анализа данных с использованием Large Language Models (LLM) через LangChain и Ollama.

## Описание

Проект представляет собой веб-приложение на Streamlit, которое автоматически выполняет полный цикл анализа данных:

1. **Загрузка данных** - поддержка CSV и Excel файлов
2. **Анализ структуры** - автоматическое определение типов данных и структуры
3. **Генерация плана метрик** - создание плана статистических метрик для анализа
4. **Расчет метрик** - автоматическая генерация и выполнение кода для расчета метрик
5. **Анализ результатов** - интерпретация метрик с помощью LLM
6. **Визуализация** - генерация графиков для визуализации данных
7. **Итоговый отчет** - создание структурированного аналитического отчета

## Архитектура

Проект следует модульной архитектуре с четким разделением ответственности:

- **UI Layer** (`src/ui/`) - пользовательский интерфейс на Streamlit
- **Core Layer** (`src/core/`) - бизнес-логика и оркестрация процесса
- **LLM Layer** (`src/llm/`) - интеграция с языковыми моделями
- **Data Layer** (`src/data/`) - обработка и анализ данных
- **Utils Layer** (`src/utils/`) - вспомогательные утилиты
- **Config Layer** (`config/`) - конфигурация приложения

Подробное описание архитектуры см. в [ARCHITECTURE.md](ARCHITECTURE.md)

## Установка

### Вариант 1: Docker (Рекомендуется)

Самый простой способ запустить приложение - использовать Docker:

1. Перейдите в директорию docker:
```bash
cd docker
```

2. Запустите сервисы:
```bash
make up
# или
docker-compose up -d
```

3. Загрузите модели Ollama:
```bash
make setup-models
# или
./setup-ollama-models.sh
```

4. Откройте приложение: http://localhost:8501

Подробнее см. [docker/README.md](docker/README.md) и [docker/QUICKSTART.md](docker/QUICKSTART.md)

### Вариант 2: Локальная установка

#### Требования

- Python 3.9+
- Ollama с установленными моделями:
  - `t-pro-it-1.0-q8_0.gguf:latest` (для анализа)
  - `qwen3-coder:latest` (для генерации кода)

#### Шаги установки

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd AI-datascientist
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения (опционально):
```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

5. Убедитесь, что Ollama запущен:
```bash
ollama serve
```

## Использование

### С Docker

```bash
cd docker
make up
# Приложение доступно на http://localhost:8501
```

### Локально

Запустите приложение:
```bash
streamlit run src/ui/main.py
```

Или если используете старую версию:
```bash
streamlit run ins_temp3.py
```

## Структура проекта

```
AI-datascientist/
├── src/                    # Основной код приложения
│   ├── ui/                 # Пользовательский интерфейс
│   ├── core/               # Бизнес-логика
│   ├── llm/                # Интеграция с LLM
│   ├── data/               # Обработка данных
│   └── utils/              # Утилиты
├── config/                 # Конфигурация
├── docker/                 # Docker конфигурация
│   ├── Dockerfile          # Production образ
│   ├── Dockerfile.dev      # Development образ
│   ├── docker-compose.yml  # Production конфигурация
│   ├── docker-compose.dev.yml  # Development конфигурация
│   └── setup-ollama-models.sh  # Скрипт загрузки моделей
├── tests/                  # Тесты
├── docs/                   # Документация
├── requirements.txt        # Зависимости
└── README.md              # Этот файл
```

## Разработка

### Добавление новых функций

1. Определите, в какой модуль добавить функциональность
2. Следуйте принципам модульной архитектуры
3. Добавьте тесты для новой функциональности
4. Обновите документацию

### Тестирование

Запуск всех unit тестов:
```bash
pytest tests/unit/ -v
```

Запуск с покрытием кода:
```bash
pytest tests/unit/ --cov=src --cov-report=html
```

Или используйте скрипт:
```bash
./scripts/run_tests.sh
./scripts/run_tests.sh --coverage
```

Подробнее см. [tests/README.md](tests/README.md)

### Форматирование кода

```bash
black src/
flake8 src/
```

## Лицензия

[Укажите лицензию]

## Контакты

[Укажите контакты]

