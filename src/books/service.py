from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from datetime import datetime

from .models import Book 
from .schemas import BookCreateModel, BookUpdateModel


class BookService:
    async def get_all_books(self, session: AsyncSession):
        stmt = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(stmt)
        books = result.all()

        return books

    async def get_book(self, book_uid: str, session: AsyncSession):
        stmt = select(Book).where(Book.uid == book_uid)
        result = await session.exec(stmt)

        book = result.first()

        return book if book is not None else None

    async def create_book(self, book_create_data: BookCreateModel, session: AsyncSession):
        book_data = book_create_data.model_dump()
        new_book = Book(**book_data)

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)

        return new_book

    async def update_book(
        self, book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uid, session)
        update_data_dict = book_update_data.model_dump()

        if book_to_update is not None:
            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)
            book_to_update.updated_at = datetime.now()
        else:
            return None

        await session.commit()

        return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()

        else:
            return None