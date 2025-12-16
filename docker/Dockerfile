# Dockerfile для AI Data Scientist приложения
FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ ./src/
COPY config/ ./config/

# Создание директории для выходных данных
RUN mkdir -p /app/outputs

# Установка переменных окружения
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Открытие порта для Streamlit
EXPOSE 8501

# Команда запуска приложения
CMD ["streamlit", "run", "src/ui/main.py", "--server.port=8501", "--server.address=0.0.0.0"]

