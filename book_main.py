from fastapi import FastAPI
from typing import List

from book_list import books
from book_models import Book

app = FastAPI()


@app.get("/books", response_model=List[Book])
async def get_all_books() -> list:
    return books


@app.post("/books")
async def create_a_book() -> dict:
    pass


@app.get("/books/{book_id}")
async def get_book(book_id: int) -> dict:
    pass


@app.patch("/books/{book_id}")
async def update_book(book_id: int) -> dict:
    pass


@app.delete("/books/{book_id}")
async def delete_book(book_id: int) -> dict:
    pass
