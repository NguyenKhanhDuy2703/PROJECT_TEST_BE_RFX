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
from app.models.task import Task, StatusEnum, PriorityEnum 
import asyncio
from datetime import datetime, timezone , timedelta
from unittest.mock import AsyncMock
from app.core.redis import redis_client
from sqlalchemy.pool import NullPool
import sys
from app.models import * 
import os
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", 
    "postgresql+asyncpg://postgres:123456@localhost:5432/rfx_db_test"
)
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
        poolclass=NullPool,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    connection = await db_engine.connect()
    transaction = await connection.begin()
    
    SessionLocal = sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )
    
    async with SessionLocal() as session:
        yield session

    await transaction.rollback()
    await connection.close()

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session
        
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
        
    app.dependency_overrides.clear()
@pytest_asyncio.fixture(scope="function", autouse=True)
async def mock_redis():
    redis_client.get = AsyncMock(return_value=None) 
    redis_client.set = AsyncMock()
    redis_client.incr = AsyncMock()
    redis_client.lpush = AsyncMock()
    redis_client.ltrim = AsyncMock()
    redis_client.delete = AsyncMock()

    yield redis_client


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
            "sub": str(test_user_admin.user_id),
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
            "sub": str(test_user_manager.user_id),
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
            "sub": str(test_user_member.user_id),
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
        joined_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    db_session.add(project_member)
    await db_session.commit()
    await db_session.refresh(project_member)
    return project_member

@pytest_asyncio.fixture(scope="function")
async def test_task_in_project(db_session, test_user_member, test_org):

    # 1. Tạo Project
    project = Project(
        name="Fixture Project for Task",
        description="A project for testing tasks",
        org_id=test_org.org_id,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)

    # 2. Add Member vào Project
    project_member = Project_member(
        project_id=project.project_id,
        user_id=test_user_member.user_id,
        joined_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    db_session.add(project_member)
    await db_session.commit()
    await db_session.refresh(project_member)

    task = Task(
        title="Fixture Task",
        description="A task for testing",
        project_id=project.project_id, 
        priority=PriorityEnum.MEDIUM, 
        status=StatusEnum.TO_DO,
        due_date=(datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7)),
        assignee_id=test_user_member.user_id, 
        create_by=test_user_member.user_id,
        create_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )

    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    
    return task

pytest_asyncio.fixture(scope="function")
async def test_prepare_reports(db_session, test_user_admin, test_project):
    project_member = Project_member(
        project_id=test_project.project_id,
        user_id=test_user_admin.user_id,
        joined_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    db_session.add(project_member)
    await db_session.commit()
    
    tasks = []
    for i in range(2):
        task = Task(
            title=f"Done Task {i+1}",
            description="Finished task",
            project_id=test_project.project_id,
            priority=PriorityEnum.LOW,
            status=StatusEnum.DONE,  # <--- Quan trọng
            due_date=(datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7)),
            assignee_id=test_user_admin.user_id,
            create_by=test_user_admin.user_id,
            create_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        db_session.add(task)
        tasks.append(task)

    for i in range(3):
        task = Task(
            title=f"Todo Task {i+1}",
            description="Task waiting",
            project_id=test_project.project_id,  
            priority=PriorityEnum.MEDIUM,
            status=StatusEnum.TO_DO, 
            due_date=(datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7)),
            assignee_id=test_user_admin.user_id,
            create_by=test_user_admin.user_id,
            create_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        db_session.add(task)
        tasks.append(task)

    task_over_due = Task(
        title="Overdue Task",
        description="This task is overdue",
        project_id=test_project.project_id,
        priority=PriorityEnum.HIGH,
        status=StatusEnum.IN_PROGRESS, 
        due_date=(datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=1)), 
        assignee_id=test_user_admin.user_id,
        create_by=test_user_admin.user_id,
        create_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(task_over_due)
    tasks.append(task_over_due)

    await db_session.commit()
    for task in tasks:
        await db_session.refresh(task)
        
    return tasks 
@pytest_asyncio.fixture(scope="function")
async def test_comment_in_task(db_session, test_task_in_project, test_user_member):
    from app.models.comment import Comment
    from datetime import datetime, timezone

    comment = Comment(
        task_id=test_task_in_project.task_id,
        content="Comment for attachment testing",
        user_id=test_user_member.user_id,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(comment)
    await db_session.commit()
    await db_session.refresh(comment)
    return comment