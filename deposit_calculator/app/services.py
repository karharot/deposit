import logging

from app.repositories import AbstractDepositRepository
from app.schemas import DepositRequest
from .deposit import calculate_deposit

logger = logging.getLogger(__name__)


class DepositService:
    def __init__(self, deposit_repository: AbstractDepositRepository):
        self.deposit_repository = deposit_repository

    async def create_deposit(self, request: DepositRequest) -> dict:
        """
        Calculates the deposit and saves it to the database.

        Args:
            request: The deposit request data.

        Returns:
            The calculated deposit result.

        Raises:
            ValueError: If the input data is invalid.
        """
        result = calculate_deposit(request.date, request.periods, request.amount, request.rate)
        deposit_data = DepositRequest(
            date=request.date,
            periods=request.periods,
            amount=request.amount,
            rate=request.rate
        )
        try:
            await self.deposit_repository.add(deposit_data)
        except Exception as e:
            logger.error(f"Error in create_deposit: {e}")
            raise
        return result
