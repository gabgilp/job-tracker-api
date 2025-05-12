from httpx import AsyncClient
import pytest
from tracker.Tests.Routers.test_authentication import login_user
from sqlalchemy import select
from tracker.database import UserTable, ApplicationTable, engine
from sqlalchemy.ext.asyncio import AsyncSession

token: str = None
updated_username = "updateduser"
user_id: int = None

@pytest.mark.anyio
@pytest.mark.order(3)
async def test_get_user_data(async_client: AsyncClient):
    global token
    global user_id
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
    user_id = response["user"]["id"]
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
        "username": updated_username
    }
    response = await async_client.put(
        "/api/user/",
        headers=headers,
        json=updated_user
    )
    response = response.json()
    
    expected_user = {
        "username": updated_username,
        "first_name": "Updated",
        "last_name": "User",
        "id": response["user"]["id"] 
    }
    assert response["user"] == expected_user
    assert response["user"]["id"] is not None
    assert response["new_token"] is not None
    token = response["new_token"]
    assert response["token_type"] == "bearer"

@pytest.mark.anyio
@pytest.mark.order(11)
async def test_delete_user(async_client: AsyncClient):
    global token
    global updated_username
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = await async_client.delete(
        "/api/user/",
        headers=headers
    )
    response = response.json()
    print(response)
    assert response["message"] == "User deleted successfully"

    async with AsyncSession(engine) as db:
        user = await db.execute(
            select(UserTable).where(UserTable.username == updated_username)
        )
        user = user.scalar_one_or_none()
        assert user is None

        applications = await db.execute(
            select(ApplicationTable).where(ApplicationTable.user_id == user_id)
        )

        applications = applications.scalars().all()
        assert len(applications) == 0
