import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.utils.config import get_settings


def add_timeout_middleware(app: FastAPI):
    @app.middleware("http")
    async def timeout_middleware(request: Request, call_next):
        timeout_seconds = get_settings().TIMEOUT  # Read dynamically for each request
        try:
            return await asyncio.wait_for(call_next(request), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            return JSONResponse(
                status_code=504,
                content={"detail": "Request timed out. Please try again later."},
            )
