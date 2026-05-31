from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    read: Optional[bool] = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    read: bool
