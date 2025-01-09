import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from sqlalchemy.orm import sessionmaker
from app.database import engine, SessionLocal


@pytest.fixture(scope='session')
async def database_engine():
    async with engine.begin() as conn:
        await conn.run_sync(SessionLocal)
    return engine


@pytest.fixture(scope='function')
async def db_session(database_engine):
    async with database_engine.connect() as connection:
        await connection.begin()
        Session = sessionmaker(bind=connection, class_=AsyncSession, expire_on_commit=False)
        async with Session() as session:
            yield session
            await session.rollback()


@pytest.fixture()
async def client(db_session):
    app.state.database_session = db_session
    with TestClient(app) as client:
        yield client
