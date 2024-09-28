# Використання базового образу Python 3.12
FROM python:3.12-slim

# Робоча директорія
WORKDIR /app

# Копіювання залежностей
COPY requirements.txt .

# Встановлення залежностей
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання решти файлів
COPY . .

# Запуск програми
CMD ["python", "main.py"]
