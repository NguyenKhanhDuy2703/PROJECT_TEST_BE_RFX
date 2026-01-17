import pytest

# Test case 1: Signup
@pytest.mark.asyncio
async def test_signup_success(client, test_org): 
    signup_data = {
        "email": "vanA@gmail.com",
        "password": "123456",
        "full_name": "Nguyen Van A",
        "org_id": test_org.org_id, 
        "role": "admin"
    }
    response = await client.post("/api/v1/users/signup", json=signup_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "vanA@gmail.com"

# Test case 2: Signin
@pytest.mark.asyncio
async def test_signin_success(client, test_org):
    signup_data = {
        "email": "vanA@gmail.com",
        "password": "123456",
        "full_name": "Nguyen Van A",
        "org_id": test_org.org_id,
        "role": "admin"
    }
    await client.post("/api/v1/users/signup", json=signup_data)
    signin_data = {
        "email": "vanA@gmail.com",
        "password": "123456",
    }
    response = await client.post("/api/v1/users/signin", json=signin_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data