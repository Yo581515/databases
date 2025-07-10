from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["persons"]

try:
    client.admin.command('ping')
    print("MongoDB is running!")
    print()
except Exception as e:
    print("MongoDB is not running:", e) 
    print()
  
    
try:
  new_collection = db["transformedPersons"]
  new_collection.drop()
  print("Collection 'transformedPersons' dropped successfully.")
  print()
except Exception as e:
  print("Error dropping collection 'transformedPersons':", e) 
  print()
  
pipeline = [
    {
        "$project": {
            "_id": 0,
            "name": 1,
            "email": 1,
            "birthdate": { "$toDate": "$dob.date" },
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
                    { "$toUpper": { "$substrCP": ["$name.first", 0, 1] } },
                    {
                        "$substrCP": [
                            "$name.first",
                            1,
                            { "$subtract": [{ "$strLenCP": "$name.first" }, 1] }
                        ]
                    },
                    " ",
                    { "$toUpper": { "$substrCP": ["$name.last", 0, 1] } },
                    {
                        "$substrCP": [
                            "$name.last",
                            1,
                            { "$subtract": [{ "$strLenCP": "$name.last" }, 1] }
                        ]
                    }
                ]
            }
        }
    },
    { "$out": "transformedPersons" }
]

result = collection.aggregate(pipeline)
print("Aggregation complete — data written to 'transformedPersons' collection.")

for doc in db["transformedPersons"].find().limit(5):
    pprint(doc)
    print()
