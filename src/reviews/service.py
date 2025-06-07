from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import List
from enum import Enum

from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService

from .schemas import ReviewCreateModel

user_service = UserService()
book_service = BookService()


class ReviewService:
    async def add_review_to_book(
        self,
        user_uid: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):

        try:
            book = await book_service.get_book(book_uid, session)

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Book not found"
                )

            if not book.user_uid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot add reviews to books without an owner",
                )

            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)
            new_review.user_uid = user_uid
            new_review.book_uid = book_uid

            session.add(new_review)
            await session.commit()

            return new_review

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops ... Something went wrong",
            )
