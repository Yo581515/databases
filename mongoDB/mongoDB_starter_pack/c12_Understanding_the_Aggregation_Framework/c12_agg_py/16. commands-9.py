from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["students"]

pipeline = [
    {
        "$project": {
            "_id": 0,
            "examScore": { "$slice": ["$examScores", 0,1] },
        }
    }
]

results = collection.aggregate(pipeline)
for doc in results:
    pprint(doc)
    print()
    