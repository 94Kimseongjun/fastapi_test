from pytrends.request import TrendReq
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import requests

from typing import List

# cmd : uvicorn main:app --reload

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GoogleTrendsKeyword(BaseModel):
    keyword: str

@app.post("/echartsBarData")
async def get_echarts_bar_data():
    response1 = requests.get('https://echarts.apache.org/examples/data/asset/data/life-expectancy-table.json')
    response2 = requests.get('https://fastly.jsdelivr.net/npm/emoji-flags@1.3.0/data.json')
    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()
        return data2,data1

@app.post("/searchGoogleTrends")
async def search_google_trends(data: GoogleTrendsKeyword):
    pytrends = TrendReq(hl="ko", tz=540)
    keyword_list = data.keyword.split(",")
    pytrends.build_payload(keyword_list, cat=0, timeframe="2023-01-01 2023-02-01", geo='KR')
    result = pytrends.interest_over_time()
    keyword_list.insert(0,'date')
    return result.to_dict()

@app.post("/reg_board/", response_model=schemas.Board)
def register_board(Board: schemas.BoardCreate, db: Session = Depends(get_db)):
    return crud.create_board(db=db, board=Board)

@app.get("/read_boards/", response_model=list[schemas.Board])
def read_boards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    boards = crud.get_boards(db, skip=skip, limit=limit)
    return boards