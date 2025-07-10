from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"] 
collection = db["students"]

pipeline = [
    {"$unwind": "$hobbies"},
    {"$group": {
        "_id": {"age": "$age"},
        "allHobbies": {"$push": "$hobbies"}
    }}
]

results = collection.aggregate(pipeline)
for doc in results:
    pprint(doc)
    print()
