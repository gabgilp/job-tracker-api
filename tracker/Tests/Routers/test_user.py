from httpx import AsyncClient
import pytest
from tracker.Tests.Routers.test_authentication import login_user

token: str = None

@pytest.mark.anyio
@pytest.mark.order(3)
async def test_get_user_data(async_client: AsyncClient):
    global token
    response = await login_user(async_client, "testuser", "testpassword")
    token = response["new_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = await async_client.get(
        "/api/user/",
        headers=headers
    )
    
    response = response.json()

    expected_user = {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "id": response["user"]["id"] 
    }

    assert response["user"] == expected_user
    assert response["user"]["id"] is not None
    assert response["new_token"] is not None
    assert response["token_type"] == "bearer"

@pytest.mark.anyio
@pytest.mark.order(10)
async def test_update_user(async_client: AsyncClient):
    global token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    updated_user = {
        "first_name": "Updated",
        "last_name": "User",
        "username": "updateduser"
    }
    response = await async_client.put(
        "/api/user/",
        headers=headers,
        json=updated_user
    )
    response = response.json()
    
    expected_user = {
        "username": "updateduser",
        "first_name": "Updated",
        "last_name": "User",
        "id": response["user"]["id"] 
    }
    assert response["user"] == expected_user
    assert response["user"]["id"] is not None
    assert response["new_token"] is not None
    assert response["token_type"] == "bearer"

@pytest.mark.anyio
@pytest.mark.order(11)
async def test_delete_user(async_client: AsyncClient):
    #TODO: Implement the test for deleting user data
    pass