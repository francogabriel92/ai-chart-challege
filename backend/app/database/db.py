import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine, text

DATABASE_URL = "postgresql://nivii-admin:1234@postgres:5432/nivii_db"

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def run_query(query: str):

    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    session = next(get_session())
    if not session:
        raise Exception("Database session not available")

    # Assuming query is a valid SQLModel query object
    result = session.exec(text(query))

    if not result:
        return []
    # Convert result to a list of dictionaries
    return [dict(row._mapping) for row in result]


SessionDep = Annotated[Session, Depends(get_session)]
