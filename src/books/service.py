from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from .models import Book
from .schemas import BookCreateModel, BookUpdateModel


class BookService:
    async def get_all_books(self, session: AsyncSession):
        stmt = select(Book).order_by(desc(Book.created_at))

    async def get_book(self, book_uid: str, session: AsyncSession):
        pass

    async def create_book(self, book_create_data: BookCreateModel, session: AsyncSession):
        pass

    async def update_book(self, book_update_data: BookUpdateModel, session: AsyncSession):
        pass

    async def update_book(self, book_uid: str, session: AsyncSession):
        pass
    
