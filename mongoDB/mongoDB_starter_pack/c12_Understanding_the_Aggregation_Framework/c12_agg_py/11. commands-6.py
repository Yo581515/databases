from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["persons"]

pipeline = [
    {
        "$project": {
            "_id": 0,
            "name": 1,
            "email": 1,
            "birthdate": {"$toDate": "$dob.date"},
            "age": "$dob.age",
            "location": {
                "type": "Point",
                "coordinates": [
                    {
                        "$convert": {
                            "input": "$location.coordinates.longitude",
                            "to": "double",
                            "onError": 0.0,
                            "onNull": 0.0
                        }
                    },
                    {
                        "$convert": {
                            "input": "$location.coordinates.latitude",
                            "to": "double",
                            "onError": 0.0,
                            "onNull": 0.0
                        }
                    }
                ]
            }
        }
    },
    {
        "$project": {
            "gender": 1,
            "email": 1,
            "location": 1,
            "birthdate": 1,
            "age": 1,
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
    },
    {
        "$group": {
            "_id": {"birthYear": {"$isoWeekYear": "$birthdate"}},
            "numPersons": {"$sum": 1}
        }
    },
    {
        "$sort": {"numPersons": -1}
    }
]

results = collection.aggregate(pipeline)
for doc in results:
    pprint(doc)
    print()

explain_data = db.command("explain", {
    "aggregate": "persons",
    "pipeline": pipeline,
    "cursor": {}
})
execution_time = explain_data["stages"][0]["$cursor"]["executionStats"]["executionTimeMillis"]
print(f"⚙️ MongoDB executionTimeMillis: {execution_time} ms")