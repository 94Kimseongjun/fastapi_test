from pytrends.request import TrendReq
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
# cmd : uvicorn main:app --reload
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GoogleTrendsKeyword(BaseModel):
    keyword: str

@app.post("/searchGoogleTrends")
async def search_google_trends(data: GoogleTrendsKeyword):
    pytrends = TrendReq(hl="ko", tz=540)
    keyword_list = data.keyword.split(",")

    pytrends.build_payload(keyword_list, cat=0, timeframe="2023-01-01 2023-02-01", geo='KR')
    result = pytrends.interest_over_time()

    keyword_list.insert(0,'date')
    #print(result.loc[:, keyword_list])
    #print(result.to_dict())
    return result.to_dict()
    #result = result.reset_index()
    #print('--------------------')
    #print(result.to_dict())