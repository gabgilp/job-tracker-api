from httpx import AsyncClient
import pytest
from tracker.Tests.Routers.test_authentication import login_user
from datetime import datetime

token: str = None
user_id: int = None
application_id: int = None

@pytest.mark.anyio
@pytest.mark.order(4)
async def test_create_application(async_client: AsyncClient):
    global token
    global user_id
    global application_id
    response = await login_user(async_client, "testuser", "testpassword")
    token = response["new_token"]
    user_id = response["user"]["id"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = await async_client.post(
        "/api/application/",
        headers=headers,
        json={
            "user_id": user_id,
            "company_name": "Test Company",
            "position_title": "Software Engineer",
            "status": "Applied",
            "notes": "Initial application",
            "date_applied": datetime(2023, 10, 1).isoformat(),
            "posting_url": "http://example.com/job"
        }
    )

    response = response.json()

    expected_application = {
        "user_id": user_id,
        "company_name": "Test Company",
        "position_title": "Software Engineer",
        "status": "Applied",
        "notes": "Initial application",
        "date_applied": datetime(2023, 10, 1).isoformat(),
        "posting_url": "http://example.com/job",
        "rejection_reason": None,
        "rejection_date": None,
        "id": response["application"]["id"]
    }

    assert response["application"] == expected_application
    assert response["application"]["id"] is not None
    application_id = response["application"]["id"]
    assert response["new_token"] is not None
    assert response["token_type"] == "bearer"


@pytest.mark.anyio
@pytest.mark.order(5)
async def test_create_application_2(async_client: AsyncClient):
    global token
    global user_id
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = await async_client.post(
        "/api/application/",
        headers=headers,
        json={
            "user_id": user_id,
            "company_name": "Test Company 2",
            "position_title": "Software Engineer 2",
            "status": "Applied",
            "notes": "Initial application 2",
            "date_applied": datetime(2023, 10, 1).isoformat(),
            "posting_url": "http://example.com/job"
        }
    )

    response = response.json()

    expected_application = {
        "user_id": user_id,
        "company_name": "Test Company 2",
        "position_title": "Software Engineer 2",
        "status": "Applied",
        "notes": "Initial application 2",
        "date_applied": datetime(2023, 10, 1).isoformat(),
        "posting_url": "http://example.com/job",
        "rejection_reason": None,
        "rejection_date": None,
        "id": response["application"]["id"]
    }

    assert response["application"] == expected_application
    assert response["application"]["id"] is not None
    assert response["new_token"] is not None
    assert response["token_type"] == "bearer"

@pytest.mark.anyio
@pytest.mark.order(6)
async def test_update_application(async_client: AsyncClient):
    global token
    global user_id
    global application_id
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = await async_client.put(
        f"/api/application/{application_id}/",
        headers=headers,
        json={
            "user_id": user_id,
            "company_name": "Updated Company",
            "position_title": "Updated Position",
            "status": "Interviewed",
            "notes": "Updated notes",
            "date_applied": datetime(2023, 10, 2).isoformat(),
            "posting_url": "http://example.com/updated_job"
        }
    )

    response = response.json()

    expected_application = {
        "user_id": user_id,
        "company_name": "Updated Company",
        "position_title": "Updated Position",
        "status": "Interviewed",
        "notes": "Updated notes",
        "date_applied": datetime(2023, 10, 2).isoformat(),
        "posting_url": "http://example.com/updated_job",
        "rejection_reason": None,
        "rejection_date": None,
        "id": application_id
    }
    assert response["application"] == expected_application
    assert response["application"]["id"] == application_id
    assert response["new_token"] is not None
    assert response["token_type"] == "bearer"

@pytest.mark.anyio
@pytest.mark.order(7)
async def test_get_application(async_client: AsyncClient):
    global token
    global application_id
    headers = {
        "Authorization": f"Bearer {token}"
    }   
    response = await async_client.get(
        f"/api/application/{application_id}/",
        headers=headers
    )
    response = response.json()
    expected_application = {
        "user_id": user_id,
        "company_name": "Updated Company",
        "position_title": "Updated Position",
        "status": "Interviewed",
        "notes": "Updated notes",
        "date_applied": datetime(2023, 10, 2).isoformat(),
        "posting_url": "http://example.com/updated_job",
        "rejection_reason": None,
        "rejection_date": None,
        "id": application_id
    }
    assert response["application"] == expected_application
    assert response["application"]["id"] == application_id
    assert response["new_token"] is not None
    assert response["token_type"] == "bearer"

@pytest.mark.anyio
@pytest.mark.order(8)
async def test_get_all_applications(async_client: AsyncClient):
    global token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = await async_client.get(
        "/api/application/all/",
        headers=headers
    )
    response = response.json()
    assert isinstance(response["applications"], list)
    assert len(response["applications"]) > 0
    assert all("id" in app for app in response["applications"])
    assert all("company_name" in app for app in response["applications"])
    assert all("position_title" in app for app in response["applications"])
    assert all("status" in app for app in response["applications"])
    assert all("notes" in app for app in response["applications"])
    assert all("date_applied" in app for app in response["applications"])
    assert all("posting_url" in app for app in response["applications"])
    assert all("rejection_reason" in app for app in response["applications"])
    assert all("rejection_date" in app for app in response["applications"])
    assert all("user_id" in app for app in response["applications"])
    assert all("id" in app for app in response["applications"])
    assert response["new_token"] is not None
    assert response["token_type"] == "bearer"
    

@pytest.mark.anyio
@pytest.mark.order(9)
async def test_delete_application(async_client: AsyncClient):
    global token
    global application_id
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = await async_client.delete(
        f"/api/application/{application_id}/",
        headers=headers
    )

    response = response.json()

    assert response["message"] == "Application deleted successfully"
    assert response["new_token"] is not None
    assert response["token_type"] == "bearer"