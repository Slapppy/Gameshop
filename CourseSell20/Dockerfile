# Используем официальный образ Python для Django
FROM python:3.9

# Устанавливаем переменную окружения для отключения интерактивных вопросов при установке
ENV PYTHONUNBUFFERED 1

# Устанавливаем poetry
RUN pip install poetry

# Создаем рабочую директорию для приложения
WORKDIR /app

# Копируем файлы зависимостей (pyproject.toml и poetry.lock) и устанавливаем зависимости с помощью poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем остальные файлы проекта
COPY . /app/

# Запускаем команду collectstatic для сбора статических файлов (если нужно)
RUN python manage.py collectstatic --noinput

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
