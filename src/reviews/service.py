from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService

from .schemas import ReviewCreateModel


class ReviewService:
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        pass
