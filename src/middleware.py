from fastapi import FastAPI
from fastapi.requests import Request

import time


def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def custom_loggin(request: Request, call_next):
        start_time = time.time()
        print("Before", start_time)

        response = await call_next(request)
        end_time = time.time() - start_time
        print("After", end_time)

        return response
