from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["c12_agg_db"]
collection = db["persons"]

print("\n📌 $bucket Example")
pipeline_bucket = [
    {
        "$bucket": {
            "groupBy": "$dob.age",
            "boundaries": [18, 22, 30, 40, 50, 60, 120],
            "output": {
                "numPersons": { "$sum": 1 },
                "averageAge": { "$avg": "$dob.age" },
                #"names": { "$push": "$name.first"},
            }
        }
    },
    {
        "$sort": { "numPersons": 1 }
    }
]
results_bucket = collection.aggregate(pipeline_bucket)
for doc in results_bucket:
    pprint(doc)
    print()

print("\n📌 $bucketAuto Example")
pipeline_bucket_auto = [
    {
        "$bucketAuto": {
            "groupBy": "$dob.age",
            "buckets": 5,
            "output": {
                "numPersons": { "$sum": 1 },
                "averageAge": { "$avg": "$dob.age" },
                #"names": { "$push": "$name.first" }
            }
        }
    }
]
results_bucket_auto = collection.aggregate(pipeline_bucket_auto)
for doc in results_bucket_auto:
    pprint(doc)
    print()





print("\n📌 Execution Stats:")
explanation = db.command({
    "explain": {
        "aggregate": "persons",
        "pipeline": pipeline_bucket,
        "cursor": {}
    },
    "verbosity": "executionStats"
})

stats = explanation["stages"][0]["$cursor"]["executionStats"]
print("Execution Time (ms):", stats["executionTimeMillis"])
print("Documents Returned:", stats["nReturned"])
print("Documents Examined:", stats["totalDocsExamined"])

# cant do this in through python :(
# db.persons.explain("executionStats").aggregate(pipeline_bucket)
