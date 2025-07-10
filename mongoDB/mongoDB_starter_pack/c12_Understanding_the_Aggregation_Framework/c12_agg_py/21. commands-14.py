from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["persons"]

pipeline = [
    { "$match": { "gender": "male" } },
    {
        "$project": {
            "_id": 0,
            "gender": 1,
            "name": { "$concat": ["$name.first", " ", "$name.last"] },
            "birthdate": { "$toDate": "$dob.date" }
        }
    },
    { "$sort": { "birthdate": 1 } },
    { "$skip": 10 },
    { "$limit": 10 }
]

results = collection.aggregate(pipeline)
for doc in results:
    pprint(doc)
    print()