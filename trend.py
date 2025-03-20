import pymongo
from datetime import datetime, timedelta
client = pymongo.MongoClient("mongodb://localhost:27017")
coll = client["crypto"]["ticker_time"]

timestamp = datetime.now().timestamp()
dt = datetime.fromtimestamp(timestamp)

# Define the time range for the same minute
start_time = dt.replace(second=0, microsecond=0)  # Start of the minute
end_time = start_time + timedelta(minutes=1)     # End of the minute
print(start_time,end_time,dt)
start_timestamp = int(start_time.timestamp())
end_timestamp = int(end_time.timestamp())

# Query documents within the same minute based on timestamp field
query = {
    "timestamp": {
        "$gte": start_timestamp,
        "$lt": end_timestamp  # Use $lt to exclude the next minute
    }
}

print("Query:", query)

dt_docs = list(coll.find(query))
print(len(dt_docs))
# for doc in dt_docs:
    # print(doc)
