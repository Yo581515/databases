from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["students"]

pipeline = [
    {
        "$project": {
            "_id": 0,
            "numScores" : { "$size": "$examScores" },
            "examScores": { "$slice": ["$examScores", 0, { "$size": "$examScores" }] }
        }
    }
]


results = collection.aggregate(pipeline)
for doc in results:
    pprint(doc)
    print()
