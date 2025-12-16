# Список файлов Docker конфигурации

## Созданные файлы

### Основные файлы

1. **Dockerfile** - Production образ приложения
   - Базовый образ: Python 3.9-slim
   - Устанавливает зависимости из requirements.txt
   - Копирует код приложения
   - Запускает Streamlit на порту 8501

2. **Dockerfile.dev** - Development образ с hot-reload
   - Аналогичен production, но без копирования кода
   - Код монтируется как volume для hot-reload

3. **Dockerfile.ollama** - Опциональный кастомный образ Ollama
   - Использует официальный образ ollama/ollama
   - Можно расширить для кастомных моделей

### Docker Compose файлы

4. **docker-compose.yml** - Production конфигурация
   - Сервис `ollama`: Ollama сервер с моделями
   - Сервис `app`: Streamlit приложение
   - Настроены healthchecks
   - Volumes для данных

5. **docker-compose.dev.yml** - Development конфигурация
   - Аналогична production, но с hot-reload
   - Монтирует исходный код как volume
   - Включает `--server.runOnSave=true` для автоперезагрузки

### Вспомогательные файлы

6. **.dockerignore** - Игнорируемые файлы при сборке
   - Исключает ненужные файлы из образа
   - Уменьшает размер образа

7. **setup-ollama-models.sh** - Скрипт загрузки моделей
   - Автоматически загружает необходимые модели Ollama
   - Проверяет статус контейнера
   - Выводит список загруженных моделей

8. **Makefile** - Удобные команды для работы с Docker
   - `make up` - запуск production
   - `make up-dev` - запуск development
   - `make down` - остановка
   - `make logs` - просмотр логов
   - И другие полезные команды

### Документация

9. **README.md** - Подробная документация
   - Описание всех файлов
   - Инструкции по использованию
   - Troubleshooting
   - Production deployment советы

10. **QUICKSTART.md** - Быстрый старт
    - Минимальные требования
    - Быстрые команды для запуска
    - Основные операции

## Использование

### Быстрый старт
```bash
cd docker
make up
make setup-models
```

### Development режим
```bash
cd docker
make up-dev
```

### Просмотр всех команд
```bash
cd docker
make help
```

## Структура сервисов

- **ollama** (порт 11434) - Ollama сервер
- **app** (порт 8501) - Streamlit приложение

## Volumes

- `ollama_data` - Данные Ollama (модели, кэш)
- `../outputs` - Выходные файлы приложения
- `../data` - Входные данные (опционально)

## Переменные окружения

Настраиваются в `docker-compose.yml`:
- `OLLAMA_BASE_URL` - URL Ollama сервера
- `OLLAMA_MODEL_ANALYST` - Модель для анализа
- `OLLAMA_MODEL_CODER` - Модель для генерации кода
- `LOG_LEVEL` - Уровень логирования
- `OUTPUT_DIR` - Директория для выходных файлов

