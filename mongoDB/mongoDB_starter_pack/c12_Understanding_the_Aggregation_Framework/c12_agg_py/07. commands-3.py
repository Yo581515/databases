from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["persons"]

pipeline = [
    {
        "$project": {
            "_id": 0,
            "gender": 1,
            "fullName": {
                "$concat": [
                    {"$toUpper": {"$substrCP": ["$name.first", 0, 1]}},
                    {
                        "$substrCP": [
                            "$name.first",
                            1,
                            {"$subtract": [{"$strLenCP": "$name.first"}, 1]}
                        ]
                    },
                    " ",
                    {"$toUpper": {"$substrCP": ["$name.last", 0, 1]}},
                    {
                        "$substrCP": [
                            "$name.last",
                            1,
                            {"$subtract": [{"$strLenCP": "$name.last"}, 1]}
                        ]
                    }
                ]
            }
        }
    }
]

results = collection.aggregate(pipeline)
for doc in results:
    pprint(doc)
    print()
