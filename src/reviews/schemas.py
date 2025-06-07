from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, conint

class ReviewResponseModel(BaseModel):
    uid: UUID 
    review_text: str
    rating: int
    user_uid: Optional[UUID]
    book_uid: Optional[UUID]
    created_at: datetime 
    updated_at: datetime 


class ReviewCreateModel(BaseModel):
    review_text: str
    rating: int
    user_uid: Optional[UUID]
    book_uid: Optional[UUID]