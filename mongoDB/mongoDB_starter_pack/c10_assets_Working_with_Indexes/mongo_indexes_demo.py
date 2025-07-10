from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from datetime import datetime
from pprint import pprint
import json
import pymongo
from datetime import UTC

print("\n📌 Module Introduction")
print("Running PyMongo version:", pymongo.__version__)
print()

client = MongoClient("mongodb://localhost:27017/")
db = client["persons_index_demo"]
collection = db["people"]
collection.drop()

with open("03. persons.json", "r", encoding="utf-8") as f:
    data = json.load(f)

collection.insert_many(data)
print("Data inserted.\n")

print("\n📌 What Are Indexes & Why Do We Use Them?")
print("Indexes help speed up queries, especially on large datasets.")
print()

print("\n📌 Adding a Single Field Index")
collection.create_index([("email", ASCENDING)])
pprint(collection.index_information()); print()

print("\n📌 Indexes Behind the Scenes")
explain = collection.find({"email": {"$regex": "@example.com$"}}).explain()
pprint(explain.get("executionStats", explain)); print()

print("\n📌 Understanding Index Restrictions")
try:
    collection.create_index([("email", ASCENDING), ("email", DESCENDING)])
except Exception as e:
    print("Index restriction error:", e)
print()

print("\n📌 Creating Compound Indexes")
collection.create_index([("location.city", ASCENDING), ("dob.age", DESCENDING)])
pprint(collection.index_information()); print()

print("\n📌 Using Indexes for Sorting")
explain = collection.find().sort("dob.age", DESCENDING).limit(3).explain()
pprint(explain.get("executionStats", explain)); print()

print("\n📌 Understanding the Default Index")
pprint(collection.index_information()); print()

print("\n📌 Configuring Indexes")
seen = set()
for doc in collection.find({}, {"login.username": 1}):
    u = doc.get("login", {}).get("username")
    if u and u in seen:
        collection.delete_one({"_id": doc["_id"]})
    elif u:
        seen.add(u)

collection.create_index([("login.username", ASCENDING)],
                        name="username_index",
                        unique=True,
                        sparse=True)
pprint(collection.index_information()); print()

print("\n📌 Understanding Partial Filters")
collection.create_index([("dob.age", ASCENDING)],
                        name="age_over_50",
                        partialFilterExpression={"dob.age": {"$gt": 50}})
pprint(collection.index_information()); print()

print("\n📌 Applying the Partial Index")
explain = collection.find({"dob.age": {"$gt": 50}}).limit(3).explain()
pprint(explain.get("executionStats", explain)); print()

print("\n📌 Understanding the Time-To-Live (TTL) Index")
for d in data:
    d["createdAt"] = datetime.now(UTC)
collection.drop()
collection.insert_many(data)
collection.create_index([("createdAt", ASCENDING)], expireAfterSeconds=60)
print("TTL index created — docs expire after 60 s.\n")

print("\n📌 Query Diagnosis & Query Planning")
explain = collection.find({"email": {"$regex": "@example.com$"}}).explain()
pprint(explain.get("executionStats", explain)); print()

print("\n📌 Understanding Covered Queries")
collection.create_index([("email", ASCENDING), ("dob.age", ASCENDING)],
                        name="cover_index")
explain = collection.find(
    {"email": {"$regex": "@example.com$"}},
    {"_id": 0, "email": 1, "dob.age": 1}
).limit(2).explain()
pprint(explain.get("executionStats", explain)); print()

print("\n📌 How MongoDB Rejects a Plan")
explain = collection.find({"email": {"$regex": "@example.com$"}}).sort("dob.age").explain()
pprint(explain.get("executionStats", explain)); print()

print("\n📌 Using Multi-Key Indexes")
collection.create_index([("location.coordinates.latitude", ASCENDING)],
                        name="multikey_index")
explain = collection.find({"location.coordinates.latitude": {"$exists": True}}).explain()
pprint(explain.get("executionStats", explain)); print()

print("\n📌 Understanding Text Indexes")
collection.create_index([("email", TEXT), ("location.city", TEXT)],
                        name="text_index")
explain = collection.find({"$text": {"$search": "example"}}).limit(2).explain()
pprint(explain.get("executionStats", explain)); print()

print("\n📌 Text Indexes & Sorting")
explain = collection.find({"$text": {"$search": "example"}}).sort("dob.age", DESCENDING).limit(2).explain()
pprint(explain.get("executionStats", explain)); print()

print("\n📌 Creating Combined Text Indexes")
collection.drop_index("text_index")
collection.create_index([("email", TEXT), ("location.state", TEXT)],
                        name="email_state_text")
print("Old text_index dropped. New combined text index created.\n")

print("\n📌 Using Text Indexes to Exclude Words")
explain = collection.find({"$text": {"$search": "example -hotmail"}}).limit(2).explain()
pprint(explain.get("executionStats", explain)); print()

print("\n📌 Setting the Default Language & Using Weights")
collection.drop_index("email_state_text")  # 👈 Drop the old text index first
collection.create_index([("email", TEXT), ("location.city", TEXT)],
                        default_language="english",
                        weights={"email": 10, "location.city": 2},
                        name="weighted_text")
print()

print("\n📌 Building Indexes")
collection.create_index([("dob.age", ASCENDING)], background=True)
print("Background index build started.\n")

print("\n📌 Wrap Up")
print("You now understand how to create, optimize, and diagnose MongoDB indexes.\n")

print("\n📌 Useful Resources & Links")
print("https://www.mongodb.com/docs/manual/indexes/\n")


collection.drop()
client.close()