import pytest
from fastapi.testclient import TestClient
import os
from typing import AsyncGenerator, Generator
import subprocess
from httpx import ASGITransport, AsyncClient
from tracker.database import engine, Base
from sqlalchemy.sql import text

# Set the environment state to "test"
os.environ["ENV_STATE"] = "test"

# Start PostgreSQL before the test session
subprocess.run(["bash", "start_postgresql.sh"], check=True)

from tracker.main import app  # noqa: E402
import tracker.database as db  # noqa: E402

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)

@pytest.fixture(scope="session", autouse=True)
async def setup_and_teardown_db() -> AsyncGenerator:
    """
    Set up the database before the test session and tear it down afterward.
    """
    try:
        # Connect to the database
        await db.database.connect()
        print("Connected to the database")

        # Initialize the database schema
        await db.init_db()
        print("Database initialized")

        yield  # Run all tests

    finally:
        # Disconnect from the database after all tests
        await db.database.disconnect()
        print("Disconnected from the database")

@pytest.fixture(scope="session", autouse=True)
def manage_postgresql():
    """
    Ensure PostgreSQL is running for the entire test session and shut it down afterward if needed.
    """
    try:
        yield  # Run all tests
    finally:
        if os.getenv("SHUTDOWN_POSTGRES") == "1":
            try:
                subprocess.run(["sudo", "systemctl", "stop", "postgresql"])
                print("PostgreSQL stopped")
            except Exception as e:
                print(f"Error stopping PostgreSQL: {e}")

@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    """
    Provide an asynchronous HTTP client for testing.
    """
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url=client.base_url) as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def truncate_database():
    """
    Truncate all tables in the database after the test session.
    """
    async with engine.begin() as conn:
        # Ensure the database schema is created before tests
        await conn.run_sync(Base.metadata.create_all)

    yield  # Run all tests

    async with engine.begin() as conn:
        # Truncate all tables after tests
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE"))
        print("Database truncated after all tests")