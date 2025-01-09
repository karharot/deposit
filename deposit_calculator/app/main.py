from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import ORJSONResponse

from app.database import get_db, engine
from sqlalchemy.orm import Session
from .deposit import calculate_deposit
from app.models import Deposit
from .schemas import DepositRequest
from typing import Dict


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    # startup
    yield
    # shutdown
    await engine.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@app.post("/calculate_deposit", response_model=Dict[str, float], status_code=200)
def calculate(request: DepositRequest, db: Session = Depends(get_db)):
    deposit_data = request.model_dump()
    db_deposit = Deposit(**deposit_data)
    db.add(db_deposit)
    db.commit()
    db.refresh(db_deposit)
    try:
        result = calculate_deposit(request.data, request.periods, request.amount, request.rate)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
