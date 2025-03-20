from fastapi import APIRouter
from datetime import datetime, timedelta
from mongo import db
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


@trendAPI.get(path="/get-market-timedelta")
async def get_market_with_timedelta(market:str,deltatime: int = 1):
    query = get_timedelta_query(market=market,deltatime=deltatime)
    print(query)
    result = coll.find(query)
    print(result)
    for res in result:
        del res["tickertime"]
        del res["_id"]
        print(res)
        return res