import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.main import app
from app.db.session import get_db
from app.models.organization import Organization
from datetime import datetime, timezone

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost:5432/rfx_db_test"

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

@pytest_asyncio.fixture(scope="function")
async def test_org(db_session):
    org = Organization(name="Fixture Corp", created_at=datetime.now(timezone.utc).replace(tzinfo=None))
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org