import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.main import app
from app.db.session import get_db
from app.models.organization import Organization
from app.models.user import User , RoleEnum
from app.models.project import Project
from app.core.security import get_password_hash , create_access_token
import asyncio
from datetime import datetime, timezone
import os
import sys
from app.models import * 
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost:5432/rfx_db_test"


@pytest.fixture(scope="session")
def event_loop():
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
@pytest_asyncio.fixture(scope="function")
async def db_engine():
   
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        future=True
    )
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    TestingSessionLocal = sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with TestingSessionLocal() as session:
        yield session
  
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session
        
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
        
    app.dependency_overrides.clear()

# create fake object for testing

@pytest_asyncio.fixture(scope="function")
async def test_org(db_session):
    org = Organization(name="Fixture Corp", created_at=datetime.now(timezone.utc).replace(tzinfo=None))
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org
@pytest_asyncio.fixture(scope="function")
async def test_user_admin(db_session, test_org):
    admin_user = User(
        email="admin@fixture.com",
        password_hash=get_password_hash("AdminPass123"),
        full_name="Fixture Admin",
        org_id=test_org.org_id,
        role=RoleEnum.ADMIN,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(admin_user)
    await db_session.commit()
    await db_session.refresh(admin_user)
    return admin_user
@pytest_asyncio.fixture(scope="function")
async def test_user_member(db_session, test_org):
    member_user = User(
        email="member@fixture.com",
        password_hash=get_password_hash("MemberPass123"),
        full_name="Fixture Member",
        org_id=test_org.org_id,
        role=RoleEnum.MEMBER,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(member_user)
    await db_session.commit()
    await db_session.refresh(member_user)
    return member_user
@pytest_asyncio.fixture(scope="function")
async def test_user_manager(db_session, test_org):
    manager_user = User(
        email="manager@fixture.com",
        password_hash=get_password_hash("ManagerPass123"),
        full_name="Fixture Manager",
        org_id=test_org.org_id,
        role=RoleEnum.MANAGER,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(manager_user)
    await db_session.commit()
    await db_session.refresh(manager_user)
    return manager_user

@pytest_asyncio.fixture(scope="function")
async def admin_auth_headers(test_user_admin):
    access_token = create_access_token(
        data={
            "user_id": test_user_admin.user_id,
            "email": test_user_admin.email,
            "role": test_user_admin.role.value
        }
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest_asyncio.fixture(scope="function")
async def manager_auth_headers(test_user_manager):
    access_token = create_access_token(
        data={
            "user_id": test_user_manager.user_id,
            "email": test_user_manager.email,
            "role": test_user_manager.role.value
        }
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest_asyncio.fixture(scope="function")
async def member_auth_headers(test_user_member):
    access_token = create_access_token(
        data={
            "user_id": test_user_member.user_id,
            "email": test_user_member.email,
            "role": test_user_member.role.value
        }
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest_asyncio.fixture(scope="function")
async def test_project(db_session, test_org):
    project = Project(
        name="Fixture Project",
        description="A project for testing",
        org_id=test_org.org_id,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
   
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)
    return project
@pytest_asyncio.fixture(scope="function")
async def test_project_member(db_session, test_project, test_user_member):
    from app.models.project_member import Project_member
    project_member = Project_member(
        project_id=test_project.project_id,
        user_id=test_user_member.user_id,
        joined_at  = datetime.now(timezone.utc).replace(tzinfo=None),
    )
    db_session.add(project_member)
    await db_session.commit()
    await db_session.refresh(project_member)
    return project_member