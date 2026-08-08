import logging

from fastapi import Request
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


async def value_error_handler(request: Request, exc: Exception):
    if isinstance(exc, ValueError):
        logger.error(f"Bad request: {exc}")
        return ORJSONResponse(
            status_code=400,
            content={"detail": {"error": str(exc)}},
        )
    logger.error(f"Unhandled exception: {exc}")
    return ORJSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"},
    )


async def db_error_handler(request: Request, exc: Exception):
    if isinstance(exc, SQLAlchemyError):
        logger.error(f"Database error: {exc}")
        return ORJSONResponse(
            status_code=500,
            content={"detail": {"error": "Internal server error during database operation"}},
        )
    logger.error(f"Unhandled exception: {exc}")
    return ORJSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"},
    )
