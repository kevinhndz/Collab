import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"

from database.almacen import Base, get_db
from main import app


@pytest.fixture(autouse=True)
def base_de_pruebas():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    sesiones = sessionmaker(bind=engine)

    def obtener_db_pruebas():
        with sesiones() as db:
            yield db

    app.dependency_overrides[get_db] = obtener_db_pruebas
    try:
        yield
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()
