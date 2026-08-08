from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories import SQLAlchemyDepositRepository
from app.services import DepositService


async def get_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyDepositRepository:
    return SQLAlchemyDepositRepository(db)


async def get_deposit_service(repo: SQLAlchemyDepositRepository = Depends(get_repository)) -> DepositService:
    return DepositService(repo)
