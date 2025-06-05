from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.books.routes import book_router


@asynccontextmanager
async def lifespan(app:FastAPI):
    print('server is starting')
    yield
    print('server is stopped')


version = "v1"

app = FastAPI(
    title="Bookly", 
    description="A REST API for book review web service", 
    version=version,
    lifespan=lifespan,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
