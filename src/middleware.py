from fastapi import FastAPI
from fastapi.requests import Request

import time
import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def custom_loggin(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        end_time = time.time() - start_time

        message = f"{request.method} - {request.url.path} - {end_time}s"

        print(message)

        return response
