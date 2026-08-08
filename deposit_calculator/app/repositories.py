from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Deposit
from app.schemas import DepositRequest


class AbstractDepositRepository(ABC):

    @abstractmethod
    async def add(self, deposit_data: DepositRequest) -> Deposit:
        raise NotImplementedError


class SQLAlchemyDepositRepository(AbstractDepositRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, deposit_data: dict) -> Deposit:
        deposit = Deposit(**deposit_data.model_dump())
        self.session.add(deposit)
        await self.session.flush()
        await self.session.commit()
        return deposit
