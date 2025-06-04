from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from typing import List

from book_list import books
from book_models import Book

app = FastAPI()


@app.get("/books", response_model=List[Book])
async def get_all_books() -> list:
    return books


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()

    books.append(new_book)

    return new_book


@app.get("/books/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.patch("/books/{book_id}")
async def update_book(book_id: int) -> dict:
    pass


@app.delete("/books/{book_id}")
async def delete_book(book_id: int) -> dict:
    pass
