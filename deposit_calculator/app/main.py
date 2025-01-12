import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, engine
from .deposit import calculate_deposit
from app.models import Deposit
from .schemas import DepositRequest
from typing import Dict

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    # startup
    yield
    # shutdown
    await engine.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    docs_url="/docs",
    lifespan=lifespan
)


@app.post("/calculate_deposit",
          response_model=Dict[str, float],
          status_code=200
          )
async def calculate(request: DepositRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = calculate_deposit(request.date, request.periods, request.amount, request.rate)
        deposit_date = {
            "date": request.date,
            "periods": request.periods,
            "amount": request.amount,
            "rate": request.rate,
        }
        db_deposit = Deposit(**deposit_date)
        logger.info(f"db_deposit: {db_deposit}")
        db.add(db_deposit)
        try:
            await db.flush()
            await db.commit()
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail={"error": "Internal server error during database operation"}
            )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": str(e)}
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
