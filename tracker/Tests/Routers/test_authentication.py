from httpx import AsyncClient
import pytest

async def create_user(client: AsyncClient, username: str, password: str) -> AsyncClient:
    response = await client.post(
        "/api/auth/register/",
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
        "/api/auth/login/",
        json={
            "username": username,
            "password": password
        }
    )
    return response.json()

@pytest.mark.anyio
@pytest.mark.order(1)
async def test_register_user(async_client: AsyncClient):
    response = await create_user(async_client, "testuser", "testpassword")

    expected_user = {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "id": response["user"]["id"]  # Dynamically include the ID
    }
    assert response["user"] == expected_user
    assert response["user"]["id"] is not None
    assert response["new_token"] is not None
    assert response["token_type"] == "bearer"



@pytest.mark.anyio
@pytest.mark.order(2)
async def test_login_user(async_client: AsyncClient):
    response = await login_user(async_client, "testuser", "testpassword")
    expected_user = {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "id": response["user"]["id"]  # Dynamically include the ID
    }
    assert response["new_token"] is not None
    assert response["token_type"] == "bearer"
    assert response["user"] == expected_user
    assert response["user"]["id"] is not None
    

