from pymongo import MongoClient, GEOSPHERE
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["transformedPersons"]

collection.create_index([("location", GEOSPHERE)])

pipeline = [
    {
        "$geoNear": {
            "near": {
                "type": "Point",
                "coordinates": [-18.4, -42.8]
            },
            "distanceField": "distance",
            "maxDistance": 1000000,
            "query": {"age": {"$gt": 30}},
            "spherical": True
        }
    },
    {
        "$limit": 10
    }
]

results = collection.aggregate(pipeline)
for doc in results:
    pprint(doc)
    print()
