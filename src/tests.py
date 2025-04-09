import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.database import Base, get_db
from src.main import app
from datetime import datetime


# Настройка базы данных для тестирования
DATABASE_URL = "postgresql+asyncpg://user:password@db/restaurant"  # Здесь необходимо заменить на свои данные
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Переопределение зависимости get_db
async def override_get_db() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Фикстура для создания и удаления таблиц для каждого теста
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Фикстура для тестового клиента
@pytest.fixture
def client(test_db):
    with TestClient(app) as client:
        yield client

# Тест кейс
# Тест не создание стола
def test_create_table(client):
    response = client.post(
        "/tables/",
        json={"name": "Test Table", "seats": 4, "location": "Window"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Table"
    assert data["seats"] == 4
    assert data["location"] == "Window"

# Тест на создание брони
def test_create_reservation(client):
    # Сперва создадим стол
    table_response = client.post(
        "/tables/",
        json={"name": "Test Table", "seats": 4, "location": "Window"}
    )
    assert table_response.status_code == 200
    table_data = table_response.json()
    table_id = table_data["id"]

    # Потом создадим бронь
    reservation_time = datetime.now().isoformat()
    response = client.post(
        "/reservations/",
        json={
            "customer_name": "Test Customer",
            "table_id": table_id,
            "reservation_time": reservation_time,
            "duration_minutes": 60
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Test Customer"
    assert data["table_id"] == table_id
    assert data["duration_minutes"] == 60

# Тест на конфликтующее бронирование
def test_create_reservation_conflict(client):
    # Создание стола
    table_response = client.post(
        "/tables/",
        json={"name": "Test Table", "seats": 4, "location": "Window"}
    )
    assert table_response.status_code == 200
    table_data = table_response.json()
    table_id = table_data["id"]

    # Создание бронирования
    reservation_time = datetime.now()
    reservation_time_str = reservation_time.isoformat()
    reservation_response = client.post(
        "/reservations/",
        json={
            "customer_name": "Test Customer 1",
            "table_id": table_id,
            "reservation_time": reservation_time_str,
            "duration_minutes": 60
        }
    )
    assert reservation_response.status_code == 200

    # Попытка создания конфликтующей брони
    conflict_reservation_time_str = reservation_time.isoformat()
    conflict_response = client.post(
        "/reservations/",
        json={
            "customer_name": "Test Customer 2",
            "table_id": table_id,
            "reservation_time": conflict_reservation_time_str,
            "duration_minutes": 60
        }
    )
    assert conflict_response.status_code == 409
    assert conflict_response.json()["detail"] == "Стол уже зарезервирован на этот временной интервал"