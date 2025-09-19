from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from main import app, get_session, SQLModel, Person
import pytest

sqlite_file_name = "test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

@pytest.fixture(name="setup_db")
def setup_db_fixture():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

def test_create_person(setup_db):
    response = client.post("/api/v1/persons", json={"name": "Alice", "age": 30, "city": "New York"})
    assert response.status_code == 201
    assert response.headers["Location"] == "/api/v1/persons/1"
    assert response.json() is None

def test_get_all_persons(setup_db):
    client.post("/api/v1/persons", json={"name": "Alice", "age": 30, "city": "New York"})
    client.post("/api/v1/persons", json={"name": "Bob", "age": 25, "city": "London"})
    response = client.get("/api/v1/persons")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["name"] == "Bob"

def test_get_person(setup_db):
    post_response = client.post("/api/v1/persons", json={"name": "Charlie", "age": 40, "city": "Paris"})
    location = post_response.headers["Location"]
    person_id = location.split("/")[-1]
    get_response = client.get(f"/api/v1/persons/{person_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Charlie"

def test_get_person_not_found(setup_db):
    response = client.get("/api/v1/persons/999")
    assert response.status_code == 404

def test_update_person(setup_db):
    post_response = client.post("/api/v1/persons", json={"name": "David", "age": 50, "city": "Berlin"})
    location = post_response.headers["Location"]
    person_id = location.split("/")[-1]
    update_response = client.patch(f"/api/v1/persons/{person_id}", json={"age": 51})
    assert update_response.status_code == 200
    assert update_response.json()["age"] == 51

def test_delete_person(setup_db):
    post_response = client.post("/api/v1/persons", json={"name": "Eve", "age": 60, "city": "Tokyo"})
    location = post_response.headers["Location"]
    person_id = location.split("/")[-1]
    delete_response = client.delete(f"/api/v1/persons/{person_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Person deleted successfully"}
    
    get_response = client.get(f"/api/v1/persons/{person_id}")
    assert get_response.status_code == 404
