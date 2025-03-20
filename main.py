from fastapi import FastAPI
from contextlib import asynccontextmanager
import pymongo
from schedulers import jobs
from trends import trends

app = FastAPI()
app.include_router(jobs.scheduledAPI)
app.include_router(trends.trendAPI)


client = pymongo.MongoClient("mongodb://localhost:27017")
coll = client["crypto"]["ticker_time"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    jobs.scheduler.start()
    yield
    jobs.scheduler.shutdown()

@app.get("/")
async def root():
    return {"greeting":"Hello world"}

@app.get("/ticker/{market}")
async def get_market(market: str):
   result = coll.find({"market":market})
   return result[0]["market"]
