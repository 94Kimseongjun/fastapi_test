from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

def get_boards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Board).offset(skip).limit(limit).all()

def get_board(db: Session, id: int):
    return db.query(models.Board).filter(models.Board.id == id).first()

def create_board(db: Session, board: schemas.BoardCreate):

    db_board = models.Board(writer=board.writer,
                            title=board.title,
                            content=board.content,
                            password=board.password,
                            reg_date=datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
                            modify_date=datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                            )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board
