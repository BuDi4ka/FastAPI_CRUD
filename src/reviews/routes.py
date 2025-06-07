from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from enum import Enum

from src.db.models import User
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer
from src.books.service import BookService

from .schemas import ReviewCreateModel, ReviewResponseModel
from .service import ReviewService


review_router = APIRouter()
review_service = ReviewService()
book_service = BookService()
access_token_bearer = AccessTokenBearer()


# @review_router.post("/book/{book_uid}", response_model=ReviewResponseModel)
# async def add_review_to_book(
#     book_uid: str,
#     review_data: ReviewCreateModel,
#     token_details: dict = Depends(access_token_bearer),
#     session: AsyncSession = Depends(get_session),
# ):
#     user_uid = token_details.get("user")["user_uid"]

#     new_review = await review_service.add_review_to_book(
#         user_uid, book_uid, review_data, session
#     )

#     return new_review

@review_router.post("/add", response_model=ReviewResponseModel)
async def add_review(
    review_data: ReviewCreateModel,
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session),
):
    user_uid = token_details.get("user")["user_uid"]
    
    # Get user's books and create enum choices
    books = await book_service.get_user_books(user_uid, session)
    choices = {book.title: str(book.uid) for book in books}
    
    if not choices:
        raise HTTPException(
            status_code=400,
            detail="You don't have any books to review"
        )
    
    # Create dynamic enum
    BookChoice = Enum('BookChoice', choices)
    
    # Update schema with available choices
    ReviewCreateModel.model_rebuild()
    ReviewCreateModel.__fields__['book_uid'].type_ = BookChoice
    
    new_review = await review_service.add_review_to_book(
        user_uid=user_uid,
        review_data=review_data,
        session=session
    )
    
    return new_review
