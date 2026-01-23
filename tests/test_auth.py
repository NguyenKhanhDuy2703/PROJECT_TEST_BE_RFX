import pytest
from app.models.user import User, RoleEnum
from app.core.security import get_password_hash, create_access_token
from datetime import datetime, timezone

# Case 01 : Create account with role admin (Direct DB Insertion)
@pytest.mark.asyncio
async def test_create_admin_account(db_session, test_org):
    admin_user = User(
        email="admin@company.com",
        password_hash=get_password_hash("AdminPass123!"),
        full_name="Super Admin",
        org_id=test_org.org_id,
        role=RoleEnum.ADMIN, 
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
   
    db_session.add(admin_user)
    await db_session.commit()
    await db_session.refresh(admin_user)

    assert admin_user.user_id is not None
    assert admin_user.role == RoleEnum.ADMIN

# Case 02 : Create account with role manager 
@pytest.mark.asyncio
async def test_create_manager_account(client, db_session, test_org):
    admin_user = User(
        email="admin_m@company.com", 
        password_hash=get_password_hash("AdminPass123!"),
        full_name="Super Admin",
        org_id=test_org.org_id,
        role=RoleEnum.ADMIN, 
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    
    db_session.add(admin_user)
    await db_session.commit()
    await db_session.refresh(admin_user)
    # 2. Setup Token 
    token = create_access_token(
        data={"user_id": admin_user.user_id, "role": admin_user.role.value} 
    )
    headers = {"Authorization": f"Bearer {token}"}

    manager_data = {
        "email": "manager1@gmail.com",
        "password": "ManagerPass123!",
        "full_name": "Manager One",
        "org_id": test_org.org_id,
        "role": "manager" 
    }
    
   
    response = await client.post("/api/v1/users/signup", json=manager_data, headers=headers)
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["email"] == "manager1@gmail.com"
    assert response_data["role"] == "manager"

# Case 03 : Create account with role member
@pytest.mark.asyncio
async def test_create_user_account(client, db_session, test_org): 
   
    admin_user = User(
        email="admin_u@gmail.com",
        password_hash=get_password_hash("AdminPass123!"),
        full_name="Super Admin",
        org_id=test_org.org_id,
        role=RoleEnum.ADMIN,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(admin_user)
    await db_session.commit()
    await db_session.refresh(admin_user)

    token = create_access_token(
        data={"user_id": admin_user.user_id, "role": admin_user.role.value}
    )
    headers = {"Authorization": f"Bearer {token}"}

    member_data = {
        "email": "member@gmail.com",
        "password": "UserPass123!",
        "full_name": "User One",
        "org_id": test_org.org_id,
        "role": "member", 
    }
    
    response = await client.post("/api/v1/users/signup", json=member_data, headers=headers)
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["email"] == "member@gmail.com"
    assert response_data["role"] == "member"

# Case 04 : Signin with correct credentials ( admin account )
@pytest.mark.asyncio
async def test_signin_admin_account(client, db_session, test_org):
    admin_user = User(
        email="admin@company.com",
        password_hash=get_password_hash("AdminPass123!"),
        full_name="Super Admin",
        org_id=test_org.org_id,
        role=RoleEnum.ADMIN, 
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
   
    db_session.add(admin_user)
    await db_session.commit()
    await db_session.refresh(admin_user)

    assert admin_user.user_id is not None
    assert admin_user.role == RoleEnum.ADMIN

    login_data = {
        "email": "admin@company.com",
        "password": "AdminPass123!"
    }
    response = await client.post("/api/v1/users/signin", json=login_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"

# case 05 : Signin with correct credentials (manager) 
@pytest.mark.asyncio
async def test_signin_manager_success(client, db_session, test_org):
    manager = User(
        email="manager_login@rfx.com",
        password_hash=get_password_hash("ManagerPass123"), 
        full_name="Manager Signin Test",
        org_id=test_org.org_id,
        role=RoleEnum.MANAGER,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(manager)
    await db_session.commit()
    login_data = {
        "email": "manager_login@rfx.com",
        "password": "ManagerPass123"
    }
    response = await client.post("/api/v1/users/signin", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# case 06 : Signin with correct credentials (member)
@pytest.mark.asyncio
async def test_signin_member_success(client, db_session, test_org):
    member = User(
        email="member_login@rfx.com",
        password_hash=get_password_hash("MemberPass123"),
        full_name="Member Signin Test",
        org_id=test_org.org_id,
        role=RoleEnum.MEMBER,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(member)
    await db_session.commit()
    login_data = {
        "email": "member_login@rfx.com",
        "password": "MemberPass123"
    }
    response = await client.post("/api/v1/users/signin", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

# case 07 : Signin fail cases 
@pytest.mark.asyncio
async def test_signin_admin_incorrect_password(client, db_session, test_org):
    admin = User(
        email="admin_fail@rfx.com",
        password_hash=get_password_hash("AdminTrue"),
        full_name="Admin Fail Test",
        org_id=test_org.org_id,
        role=RoleEnum.ADMIN,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(admin)
    await db_session.commit()
    login_data = {
        "email": "admin_fail@rfx.com",
        "password": "AdminWrong" 
    }
    response = await client.post("/api/v1/users/signin", json=login_data)
    assert response.status_code == 401
    assert response.json()["message"] == "Incorrect email or password"

# case 08 : Signin fail - email not found
@pytest.mark.asyncio
async def test_signin_manager_email_not_found(client, db_session):
    login_data = {
        "email": "ghost_manager@rfx.com", 
        "password": "AnyPassword"
    }
    response = await client.post("/api/v1/users/signin", json=login_data)
    assert response.status_code == 401

#case 09 : Signin fail - incorrect password for member
@pytest.mark.asyncio
async def test_signin_member_incorrect_password(client, db_session, test_org):
    member = User(
        email="member_fail@rfx.com",
        password_hash=get_password_hash("MemberPassTrue"),
        full_name="Member Fail",
        org_id=test_org.org_id,
        role=RoleEnum.MEMBER,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(member)
    await db_session.commit()

    login_data = {
        "email": "member_fail@rfx.com",
        "password": "WrongPassword123"
    }
    response = await client.post("/api/v1/users/signin", json=login_data)

    assert response.status_code == 401