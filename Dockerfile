# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /test_task_Hitalent

# Копируем файлы в контейнер
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запускаем приложение
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]