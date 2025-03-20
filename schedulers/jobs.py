from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import APIRouter
from mongo import *
from datetime import datetime
import requests
coll = db["ticker_time"]

url = "https://api.coindcx.com/exchange/ticker"

scheduledAPI = APIRouter(prefix="/schedule",tags=["scheduled"])


def filer_data(data):
    for i in range(len(data)):
        data[i].update({"tickertime":datetime.now()})
    return data

def get_ticker():
    data = requests.get(url).json()
    data = filer_data(data=data)
    return data

@scheduledAPI.post("/ticker-save")
async def ticker_save():
    data = get_ticker()
    coll.insert_many(data)
    return "success"

def call_scheduled_job_api():
    requests.post(url="http://127.0.0.1:8000/schedule/ticker-save",data={})

scheduler = BackgroundScheduler()
scheduler.add_job(call_scheduled_job_api,"interval",seconds=60,max_instances=1)
scheduler.start()



