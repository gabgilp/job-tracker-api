from httpx import AsyncClient
import pytest

async def create_user(client: AsyncClient, username: str, password: str) -> AsyncClient:
    response = await client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": password,
            "first_name": "Test",
            "last_name": "User"
        }
    )
    return response.json()


async def login_user(client: AsyncClient, username: str, password: str) -> AsyncClient:
    response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password
        }
    )
    return response.json()

@pytest.mark.anyio
async def test_register_user(async_client: AsyncClient):
    response = await create_user(async_client, "testuser", "testpassword")
    assert response["message"] == "User registered successfully"



@pytest.mark.anyio
async def test_login_user(async_client: AsyncClient):
    response = await login_user(async_client, "testuser", "testpassword")
    assert response["access_token"] is not None
    assert response["token_type"] == "bearer"
