from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["students"]

pipeline = [
    { "$unwind": "$examScores" },
    { "$project": { "_id": 1, "name": 1, "age": 1, "score": "$examScores.score" } },
    { "$sort": { "score": -1 } },
    {
        "$group": {
            "_id": "$_id",
            "name": { "$first": "$name" },
            "maxScore": { "$max": "$score" }
        }
    },
    { "$sort": { "maxScore": -1 } }
]

results = collection.aggregate(pipeline)

for doc in results:
    pprint(doc)
    print()