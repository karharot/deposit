from fastapi import APIRouter, Depends
from app.services import DepositService
from app.schemas import DepositRequest
from app.dependencies import get_deposit_service
from typing import Dict
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/calculate_deposit",
             response_model=Dict[str, float],
             status_code=200
             )
async def calculate_deposit_endpoint(
    request: DepositRequest,
    deposit_service: DepositService = Depends(get_deposit_service)
):
    result = await deposit_service.create_deposit(request)
    return result
