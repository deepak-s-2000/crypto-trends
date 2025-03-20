import requests
import pymongo
from datetime import datetime,timedelta,timezone
import time
import logging
url = "https://api.coindcx.com/exchange/ticker"
client = pymongo.MongoClient("mongodb://localhost:27017")
# coll = client["crypto"]["coin_ticker"]
def filer_data(data):
    for i in range(len(data)):
        data[i].update({"tickertime":datetime.now()})
    return data

coll = client["crypto"]["ticker_time"]
i = 0
while i < 60:
    data = requests.get(url).json()
    data = filer_data(data=data)
    coll.insert_many(data)
    # delt = datetime.now() - timedelta(minutes=2)
    # delete_query = {"timestamp":{"$lt":delt.timestamp()}}
    # coll.delete_many(delete_query)
    time.sleep(60)
    i+=1
    print(i,len(data))