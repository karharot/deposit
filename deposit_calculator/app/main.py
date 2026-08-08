import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.routers import router
from app.errors import value_error_handler, db_error_handler
from app.database import engine

logging.basicConfig(level=logging.INFO)
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
    lifespan=lifespan,
)

app.include_router(router)

app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(SQLAlchemyError, db_error_handler)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
