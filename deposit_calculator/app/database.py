import os

import yaml
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base


CONFIG_FILE = "config.yaml"


def get_database_url():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return database_url

    try:
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)
            database_url = config.get("DATABASE_URL")
            if database_url:
                return database_url
    except FileNotFoundError:
        print(f"Warning: Configuration file {CONFIG_FILE} not found.")
    except Exception as e:
        print(f"Error reading configuration file: {e}")


DATABASE_URL = get_database_url()

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        yield db
