from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class BoardBase(BaseModel):
    writer: str
    title: str
    content: str
    password: str


class Board(BoardBase):
    id: int
    view_count: int
    reg_date: datetime
    modify_date: datetime
    class Config:
        orm_mode = True

class BoardCreate(BoardBase):
    pass