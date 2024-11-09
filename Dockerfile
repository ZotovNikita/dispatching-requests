# Используем официальный образ Python
FROM python:3.12.5

# Установим рабочую директорию
WORKDIR ./backend

# Скопируем файлы зависимостей в рабочую директорию
COPY requirements.txt requirements.txt

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем все остальные файлы проекта в рабочую директорию
COPY . .

# Укажем команду для запуска приложения Streamlit
CMD ["python", "-m", "src"]
