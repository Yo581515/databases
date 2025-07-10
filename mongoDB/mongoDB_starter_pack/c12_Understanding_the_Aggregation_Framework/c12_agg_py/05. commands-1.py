from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["persons"]

pipeline = [
    {"$match": {"gender": "female"}},
    {"$group": {
        "_id": {"state": "$location.state"},
        "totalPersons": {"$sum": 1}
    }}
]

results = collection.aggregate(pipeline)
for doc in results:
    pprint(doc)
    print()