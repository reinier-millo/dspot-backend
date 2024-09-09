"""
Pytest configuration
"""
from typing import Generator
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from app.db.config import engine, SessionLocal
from app.main import app


@pytest.fixture(scope="class")
def db_session() -> Generator[Session, None, None]:
    """
    Create a new database session for the test
    """
    # Configure the Alembic settings to indicate that we are running in test mode
    config = AlembicConfig("alembic.ini")

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


@pytest.fixture(scope="class")
def test_client():
    """
    Create a new test client for the API
    """
    with TestClient(app=app) as client:
        yield client
