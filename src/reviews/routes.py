from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer


from .schemas import ReviewCreateModel, ReviewResponseModel
from .service import ReviewService


review_router = APIRouter()
review_service = ReviewService()
access_token_bearer = AccessTokenBearer()


@review_router.post("/book/{book_uid}", response_model=ReviewResponseModel)
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session),
):
    user_uid = token_details.get("user")["user_uid"]

    new_review = await review_service.add_review_to_book(
        user_uid, book_uid, review_data, session
    )

    return new_review
