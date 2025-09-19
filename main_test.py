# test_main.py
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from main import app, get_session, SQLModel, Person
import pytest

# Создаем движок базы данных для тестов в памяти (SQLite)
# Это гарантирует, что тесты не будут зависеть от внешней БД
sqlite_file_name = "test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

# Переопределяем зависимость get_session для тестов
# Это позволяет использовать тестовую БД при каждом запросе
def override_get_session():
    with Session(engine) as session:
        yield session

# Применяем переопределенную зависимость к приложению
app.dependency_overrides[get_session] = override_get_session

# Создаем тестового клиента
client = TestClient(app)

# Фикстура, которая создает таблицы перед каждым тестом и удаляет после
@pytest.fixture(name="setup_db")
def setup_db_fixture():
    # Создаем таблицы
    SQLModel.metadata.create_all(engine)
    yield
    # Удаляем таблицы после теста
    SQLModel.metadata.drop_all(engine)

# -------------
# ТЕСТЫ API
# -------------

# Тест POST /api/v1/persons - создание записи
def test_create_person(setup_db):
    response = client.post("/api/v1/persons", json={"name": "Alice", "age": 30, "city": "New York"})
    assert response.status_code == 201
    assert response.headers["Location"] == "/api/v1/persons/1"
    assert response.json() is None  # Должно быть пустое тело

# Тест GET /api/v1/persons - получение всех записей
def test_get_all_persons(setup_db):
    client.post("/api/v1/persons", json={"name": "Alice", "age": 30, "city": "New York"})
    client.post("/api/v1/persons", json={"name": "Bob", "age": 25, "city": "London"})
    response = client.get("/api/v1/persons")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["name"] == "Bob"

# Тест GET /api/v1/persons/{personId} - получение одной записи
def test_get_person(setup_db):
    post_response = client.post("/api/v1/persons", json={"name": "Charlie", "age": 40, "city": "Paris"})
    # Поскольку POST теперь возвращает пустое тело, нужно получить ID из Location header
    location = post_response.headers["Location"]
    person_id = location.split("/")[-1]
    get_response = client.get(f"/api/v1/persons/{person_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Charlie"

# Тест GET /api/v1/persons/{personId} - когда запись не найдена
def test_get_person_not_found(setup_db):
    response = client.get("/api/v1/persons/999")
    assert response.status_code == 404

# Тест PATCH /api/v1/persons/{personId} - обновление записи
def test_update_person(setup_db):
    post_response = client.post("/api/v1/persons", json={"name": "David", "age": 50, "city": "Berlin"})
    location = post_response.headers["Location"]
    person_id = location.split("/")[-1]
    update_response = client.patch(f"/api/v1/persons/{person_id}", json={"age": 51})
    assert update_response.status_code == 200
    assert update_response.json()["age"] == 51

# Тест DELETE /api/v1/persons/{personId} - удаление записи
def test_delete_person(setup_db):
    post_response = client.post("/api/v1/persons", json={"name": "Eve", "age": 60, "city": "Tokyo"})
    location = post_response.headers["Location"]
    person_id = location.split("/")[-1]
    delete_response = client.delete(f"/api/v1/persons/{person_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Person deleted successfully"}
    
    # Проверяем, что запись действительно удалена
    get_response = client.get(f"/api/v1/persons/{person_id}")
    assert get_response.status_code == 404
