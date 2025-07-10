from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["persons"]

pipeline = [
    {
        "$match": {
            "dob.age": {"$gt": 50}
        }
    },
    {
        "$group": {
            "_id": {"gender": "$gender"},
            "totalPersons": {"$sum": 1},
            "avgAge": {"$avg": "$dob.age"},
        }
    }, 
    {
        "$sort": {"totalPersons": -1}
    }
]


results = collection.aggregate(pipeline)
results = list(results)[:5]
for doc in results:
    pprint(doc)
    print()
