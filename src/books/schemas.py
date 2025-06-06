from pydantic import BaseModel
from uuid import UUID

from datetime import datetime, date
from typing import Optional, List

from src.reviews.schemas import ReviewResponseModel


class Book(BaseModel):
    uid: UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[UUID]
    created_at: datetime
    updated_at: datetime


class BookDetailModel(Book):
    reviews: List[ReviewResponseModel]


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    
