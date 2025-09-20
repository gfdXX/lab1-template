import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Response, status, Depends
from sqlmodel import Field, SQLModel, Session, create_engine, select

database_url = os.getenv("DATABASE_URL", "postgresql://program:test@postgres:5432/persons")
engine = create_engine(database_url, echo=True)
print("HELLO")

class PersonBase(SQLModel):
    name: str = Field(index=True)
    age: int
    address: str
    work: str

class Person(PersonBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class PersonCreate(PersonBase):
    pass

class PersonRead(PersonBase):
    id: int

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="RSOi Lab1 API", 
    description="API для управления людьми",
    version="1.0.0",
    lifespan=lifespan
)

print("HELLO2")

@app.get("/")
def root():
    return {"message": "RSOi Lab1 API is running", "docs": "/docs"}

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/api/v1/persons", response_model=List[PersonRead])
def get_all_persons(session: Session = Depends(get_session)):
    persons = session.exec(select(Person)).all()
    return persons

@app.post("/api/v1/persons", status_code=status.HTTP_201_CREATED)
def create_person(person: PersonCreate, response: Response, session: Session = Depends(get_session)):
    new_person = Person.model_validate(person)
    session.add(new_person)
    session.commit()
    session.refresh(new_person)
    response.headers["Location"] = f"/api/v1/persons/{new_person.id}"
    return None

@app.get("/api/v1/persons/{personId}", response_model=PersonRead)
def get_person(personId: int, session: Session = Depends(get_session)):
    person = session.get(Person, personId)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person

@app.patch("/api/v1/persons/{personId}", response_model=PersonRead)
def update_person(personId: int, person_update: dict, session: Session = Depends(get_session)):
    person = session.get(Person, personId)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    person_data = person_update
    for field, value in person_data.items():
        setattr(person, field, value)
    session.add(person)
    session.commit()
    session.refresh(person)
    return person

@app.delete("/api/v1/persons/{personId}")
def delete_person(personId: int, session: Session = Depends(get_session)):
    person = session.get(Person, personId)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    session.delete(person)
    session.commit()
    return {"message": "Person deleted successfully"}