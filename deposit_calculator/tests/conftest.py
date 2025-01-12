import pytest_asyncio
from starlette.testclient import TestClient

from app.main import app
from app.database import engine, SessionLocal


@pytest_asyncio.fixture(scope='session')
async def database_engine():
    return engine


@pytest_asyncio.fixture(scope='function')
async def db_session(database_engine):
    async with SessionLocal() as session:
        async with session.begin():
            yield session
            await session.rollback()


@pytest_asyncio.fixture
async def client(db_session):
    app.state.database_session = db_session
    with TestClient(app) as client:
        yield client
