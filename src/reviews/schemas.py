from datetime import datetime
from typing import Optional, Annotated
from uuid import UUID
from pydantic import BaseModel, Field

class ReviewResponseModel(BaseModel):
    uid: UUID 
    review_text: str
    rating: int
    user_uid: UUID
    book_uid: UUID
    created_at: datetime 
    updated_at: datetime 


class ReviewCreateModel(BaseModel):
    review_text: str
    rating: Annotated[int, Field(ge=1, le=5)]
