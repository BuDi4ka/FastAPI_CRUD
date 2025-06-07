# from datetime import datetime
# from typing import Optional, Annotated
# from uuid import UUID
# from pydantic import BaseModel, Field

# class ReviewResponseModel(BaseModel):
#     uid: UUID 
#     review_text: str
#     rating: int
#     user_uid: UUID
#     book_uid: UUID
#     created_at: datetime 
#     updated_at: datetime 


# class ReviewCreateModel(BaseModel):
#     review_text: str
#     rating: Annotated[int, Field(ge=1, le=5)]

from datetime import datetime
from typing import Optional, Annotated, List
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum

class BookChoice(str, Enum):
    """This will be dynamically populated with user's books"""
    pass

class ReviewResponseModel(BaseModel):
    uid: UUID 
    review_text: str
    rating: int
    user_uid: UUID
    book_uid: UUID
    created_at: datetime 
    updated_at: datetime 


class ReviewCreateModel(BaseModel):
    book_uid: BookChoice = Field(
        ..., 
        description="Choose a book to review from your library"
    )
    review_text: str = Field(
        ..., 
        description="Your review text",
        min_length=10,
        max_length=500
    )
    rating: int = Field(
        ..., 
        description="Rate the book from 1 to 5",
        ge=1, 
        le=5
    )

