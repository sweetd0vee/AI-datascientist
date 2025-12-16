# Docker конфигурация для AI Data Scientist

Этот каталог содержит Docker конфигурацию для контейнеризации приложения и Ollama.

## Структура

- `Dockerfile` - Production образ приложения
- `Dockerfile.dev` - Development образ с hot-reload
- `Dockerfile.ollama` - Опциональный кастомный образ Ollama
- `docker-compose.yml` - Production конфигурация
- `docker-compose.dev.yml` - Development конфигурация
- `.dockerignore` - Игнорируемые файлы при сборке

## Быстрый старт

### Production режим

1. Запуск всех сервисов:
```bash
cd docker
docker-compose up -d
```

2. Приложение будет доступно по адресу: http://localhost:8501
3. Ollama будет доступен по адресу: http://localhost:11434

4. Остановка сервисов:
```bash
docker-compose down
```

### Development режим

1. Запуск в режиме разработки (с hot-reload):
```bash
cd docker
docker-compose -f docker-compose.dev.yml up
```

2. Изменения в коде будут автоматически подхватываться Streamlit

3. Остановка:
```bash
docker-compose -f docker-compose.dev.yml down
```

## Подготовка моделей Ollama

Перед первым запуском необходимо загрузить модели в Ollama:

```bash
# Подключиться к контейнеру Ollama
docker exec -it ai-datascientist-ollama bash

# Или выполнить команды напрямую
docker exec ai-datascientist-ollama ollama pull t-pro-it-1.0-q8_0.gguf:latest
docker exec ai-datascientist-ollama ollama pull qwen3-coder:latest
```

Или выполнить скрипт подготовки:
```bash
./docker/setup-ollama-models.sh
```

## Переменные окружения

Переменные окружения можно настроить в `docker-compose.yml` или через `.env` файл:

```env
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL_ANALYST=t-pro-it-1.0-q8_0.gguf:latest
OLLAMA_MODEL_CODER=qwen3-coder:latest
OLLAMA_TEMPERATURE_ANALYST=0.55
OLLAMA_TEMPERATURE_CODER=0.2
LOG_LEVEL=INFO
OUTPUT_DIR=/app/outputs
```

## Volumes

- `ollama_data` - Данные Ollama (модели, кэш)
- `../outputs` - Выходные файлы приложения (графики, отчеты)
- `../data` - Входные данные (опционально)

## Полезные команды

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Только приложение
docker-compose logs -f app

# Только Ollama
docker-compose logs -f ollama
```

### Пересборка образов
```bash
docker-compose build --no-cache
```

### Очистка
```bash
# Остановка и удаление контейнеров
docker-compose down

# Удаление volumes (включая модели Ollama!)
docker-compose down -v

# Удаление образов
docker-compose down --rmi all
```

### Проверка здоровья сервисов
```bash
# Проверка статуса
docker-compose ps

# Проверка здоровья Ollama
curl http://localhost:11434/api/tags

# Проверка здоровья приложения
curl http://localhost:8501/_stcore/health
```

## Troubleshooting

### Ollama не запускается
- Проверьте, что порт 11434 свободен: `lsof -i :11434`
- Проверьте логи: `docker-compose logs ollama`

### Приложение не может подключиться к Ollama
- Убедитесь, что используется правильный URL: `http://ollama:11434` (внутри Docker сети)
- Проверьте, что сервис `ollama` запущен: `docker-compose ps`
- Проверьте сеть: `docker network inspect ai-datascientist-network`

### Модели не загружены
- Выполните команды загрузки моделей (см. раздел "Подготовка моделей Ollama")
- Проверьте доступное место на диске для моделей

### Проблемы с правами доступа
- Убедитесь, что директория `outputs` имеет правильные права
- В Linux: `chmod -R 777 outputs/`

## Production deployment

Для production рекомендуется:

1. Использовать `.env` файл для секретов
2. Настроить reverse proxy (nginx) перед Streamlit
3. Использовать Docker secrets для чувствительных данных
4. Настроить мониторинг и логирование
5. Использовать Docker Swarm или Kubernetes для оркестрации

## Безопасность

- Не коммитьте `.env` файлы с секретами
- Используйте Docker secrets в production
- Ограничьте доступ к портам через firewall
- Регулярно обновляйте базовые образы

