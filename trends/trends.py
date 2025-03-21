from fastapi import APIRouter
from datetime import datetime, timedelta
from mongo import db
import requests
import pandas as pd
trendAPI = APIRouter(prefix="/trend",tags=["trends"])
coll = db["ticker_time"]

def get_timedelta_query(market: str,deltatime:int=1):
    # timestamp = datetime.now().timestamp()
    # dt = datetime.fromtimestamp(timestamp)
    # start_time = dt.replace(second=0, microsecond=0)  
    start_time = datetime.now() - timedelta(minutes=deltatime)
    start_time = start_time.replace(second=0,microsecond=0)
    end_time = start_time + timedelta(seconds=59)    
    # print(market,deltatime)
    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(end_time.timestamp())
    # print(timestamp,start_timestamp,end_timestamp,start_time,end_time)
    query = {
        "timestamp": {
            "$gte": start_timestamp,
            "$lt": end_timestamp  
        },
        "market":market
    }
    return query

def process_result(result):
    del result["tickertime"]
    del result["_id"]
    return result

@trendAPI.get(path="/get-market-timedelta")
async def get_market_with_timedelta(market:str,deltatime: int = 1):
    query = get_timedelta_query(market=market,deltatime=deltatime)
    print(query)
    result = coll.find(query)
    for res in result:
        process_result(result=res)
    
@trendAPI.get(path="/get-all-market-timedelta")
async def get_market_with_timedelta(deltatime: int = 1):
    query = get_timedelta_query(market="",deltatime=deltatime)
    del query["market"]
    print(query)
    result = coll.find(query)
    # print(len(result))
    response = []
    for res in result:
        resp = process_result(result=res)
        # print(resp)
        response.append(resp)
    return response

@trendAPI.get(path="/get-all-change")
def get_all_market_change(deltatime: int = 5):
    print("???????//")
    latest = requests.get("http://127.0.0.1:8000/trend/get-all-market-timedelta",
                          params={"deltatime":2}).json()
    old = requests.get("http://127.0.0.1:8000/trend/get-all-market-timedelta",
                          params={"deltatime":2+deltatime}).json()
    old_prices = {item["market"]: float(item["last_price"]) for item in old}
    new_prices = {item["market"]: float(item["last_price"]) for item in latest}
    changes = []

    for market, new_price in new_prices.items():
        if market in old_prices:
            old_price = old_prices[market]
            difference = new_price - old_price
            percentage_change = (difference / old_price) * 100 if old_price != 0 else 0
            changes.append({
                "market": market,
                "percentage_change": percentage_change
            })
    return changes

