from fastapi import FastAPI
from books import books

app = FastAPI()


@app.get("/books")
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
