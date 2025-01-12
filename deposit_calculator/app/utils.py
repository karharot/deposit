import os
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    database_url = os.getenv("DATABASE_URL")
    if database_url is None:
        raise ValueError("DATABASE_URL environment variable is not set")
    if not database_url.startswith("postgresql+asyncpg"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
    return database_url
