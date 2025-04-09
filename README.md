# API-сервис бронирования столиков в ресторане

Этот проект представляет собой REST API для бронирования столиков в ресторане, разработанный с использованием FastAPI, SQLAlchemy, PostgreSQL, Alembic и Docker.

## Запуск

1. **Установите Docker и Docker Compose.**

2. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/mrMaks2/test_task_Hitalent.git
    ```

   Необходимо исправить коннектные данные для БД PostgreSQL в файлах database.py, alembic.ini, docker-compose.yml


3. **Запустите виртуальное окружение:**

    ```bash
    venv\Scripts\activate
    ```

4. **Запустите приложение с помощью Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    Это создаст и запустит контейнеры для приложения FastAPI, PostgreSQL.


5. **Доступ к API:**


    После запуска приложение будет доступно по адресу `http://localhost:8000`.


6. **Доступ к документации Swagger:**


    Автоматически сгенерированная документация Swagger будет 
    доступна по адресу `http://localhost:8000/docs`.


## Описание проекта

Проект состоит из следующих основных компонентов:

*   **FastAPI:** Основной фреймворк для создания REST API.
*   **SQLAlchemy:** ORM для работы с базой данных PostgreSQL.
*   **PostgreSQL:** Реляционная база данных для хранения данных о столиках и бронях.
*   **Alembic:** Инструмент для управления миграциями базы данных.
*   **Docker:** Инструмент для контейнеризации приложения.
*   **Docker Compose:** Инструмент для оркестровки контейнеров.

# Структура проекта

    test_task_Hitalent
    ├── src
    │   ├── __init__.py
    │   ├── database.py       # Конфигурация базы данных и сессии
    │   ├── main.py           # Главный файл приложения FastAPI
    │   ├── models.py
    │   │   ├── __init__.py
    │   │   ├── reservations.py  # Модель SQLAlchemy бронирования
    │   │   └── tables.py        # Модель SQLAlchemy столов
    │   ├── routers
    │   │   ├── __init__.py
    │   │   ├── reservations.py  # Роуты для работы с бронями
    │   │   └── tables.py        # Роуты для работы со столами
    │   ├── schemas.py
    │   │   ├── __init__.py
    │   │   ├── reservations.py  # Схемы Pydantic для валидации данных бронирования
    │   │   └── tables.py        # Схемы Pydantic для валидации данных столов
    │   └── tests.py             # Тесты
    ├── alembic
    │   ├── versions          # Миграции базы данных
    │   └── ...
    ├── alembic.ini         # Конфигурация Alembic
    ├── docker-compose.yml  # Конфигурация Docker Compose
    ├── Dockerfile          # Файл Dockerfile для приложения
    └── README.md           # Этот файл

## API Endpoints

### Столики

*   `GET /tables/` - Получить список всех столиков.
*   `POST /tables/` - Создать новый столик.
*   `DELETE /tables/{id}` - Удалить столик по ID.

### Брони

*   `GET /reservations/` - Получить список всех броней.
*   `POST /reservations/` - Создать новую бронь.
*   `DELETE /reservations/{id}` - Удалить бронь по ID.

## Валидация бронирования

    При создании брони API проверяет, что столик не занят в указанный временной слот. 
    Если столик занят, возвращается ошибка.
