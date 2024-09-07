from app.db.config import engine, SessionLocal
import pytest
from typing import Generator
from sqlalchemy.orm import Session
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Create a new database session for the test
    """
    # Configure the Alembic settings to indicate that we are running in test mode
    config = AlembicConfig("alembic.ini")
    config.set_main_option("run_mode", "test")

    # Open connection to database and run migrations
    connection = engine.connect()
    upgrade(config, "head")

    # Create a new database session
    session = SessionLocal(bind=connection)
    yield session
    session.close()

    # Rollback the migrations and close the connection
    downgrade(config, "base")
    connection.close()


@pytest.fixture(scope="function")
def test_client():
    """
    Create a new test client for the API
    """
    with TestClient(app=app) as client:
        yield client
