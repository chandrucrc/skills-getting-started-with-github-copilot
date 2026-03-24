import pytest
from httpx import AsyncClient
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.get("/activities")
        data = response.json()
    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_and_unregister():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: Sign up
        response = await ac.post(f"/activities/{activity}/signup?email={email}")
        # Assert: Signup successful
        assert response.status_code == 200
        assert f"Signed up {email}" in response.json()["message"]

        # Act: Duplicate signup
        response2 = await ac.post(f"/activities/{activity}/signup?email={email}")
        # Assert: Should allow or error based on backend logic
        assert response2.status_code == 200 or response2.status_code == 400

        # Act: Unregister
        response3 = await ac.post(f"/activities/{activity}/unregister?email={email}")
        # Assert: Unregister successful
        assert response3.status_code == 200
        assert f"Removed {email}" in response3.json()["message"]

        # Act: Unregister again
        response4 = await ac.post(f"/activities/{activity}/unregister?email={email}")
        # Assert: Should error (participant not found)
        assert response4.status_code == 404

@pytest.mark.asyncio
async def test_signup_activity_not_found():
    # Arrange
    email = "ghost@mergington.edu"
    activity = "Nonexistent Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

@pytest.mark.asyncio
async def test_unregister_activity_not_found():
    # Arrange
    email = "ghost@mergington.edu"
    activity = "Nonexistent Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
