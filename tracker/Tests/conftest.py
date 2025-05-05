import pytest
from fastapi.testclient import TestClient
import os
from typing import AsyncGenerator, Generator
import subprocess
from httpx import ASGITransport, AsyncClient

os.environ["ENV_STATE"] = "test"

from tracker.main import app
import tracker.database as db

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)

@pytest.fixture(autouse=True)
async def setup_and_teardown_db() -> AsyncGenerator:
    try:
        await db.database.connect()
        print("Connected to the database")

        await db.init_db()
        print("Database initialized")

        yield
    finally:
        await db.database.disconnect()
        print("Disconnected from the database")

        if os.getenv("SHUTDOWN_POSTGRES") == "1":
            try:
                subprocess.run(["sudo", "systemctl", "stop", "postgresql"])
                print("PostgreSQL stopped")
            except Exception as e:
                print(f"Error stopping PostgreSQL: {e}")

@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url=client.base_url) as ac:
        yield ac