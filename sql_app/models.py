from sqlalchemy import Column,  Integer, String, DateTime
from datetime import datetime
from .database import Base

class Board(Base):
    __tablename__ = 'BOARD'
    id = Column(Integer, primary_key=True, index=True)
    writer = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    reg_date = Column(DateTime(timezone=True), nullable=False)
    modify_date = Column(DateTime(timezone=True), nullable=False)
    password = Column(String, nullable=True)
    view_count = Column(Integer, default=0)


