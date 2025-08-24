# Указываем базовый образ
FROM python:3.13

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

 # Создаем директорию для медиафайлов и статики
RUN mkdir -p /app/media /app/static && chmod -R 755 /app

 # Пробрасываем порт, который будет использовать Django
EXPOSE 8000
