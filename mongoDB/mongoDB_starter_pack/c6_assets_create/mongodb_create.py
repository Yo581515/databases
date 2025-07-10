from pymongo import MongoClient, WriteConcern
from pymongo.errors import BulkWriteError
import json
from pprint import pprint

print("\n📌 Module Introduction")

client = MongoClient("mongodb://localhost:27017/")
db = client["tv_database"]
collection = db["tv_shows"]
collection.drop()

print("\n📌 Creating Documents - An Overview")
sample_show = {
    "title": "Example Show",
    "language": "English",
    "genres": ["Drama", "Mystery"],
    "rating": {"average": 8.4}
}
collection.insert_one(sample_show)
pprint(collection.find_one({"title": "Example Show"}))

print("\n📌 Understanding \"insert()\" Methods")
collection.insert_many([
    {"title": "Show A", "language": "English"},
    {"title": "Show B", "language": "Japanese"}
])
for show in collection.find({"title": {"$in": ["Show A", "Show B"]}}):
    pprint(show)

print("\n📌 Working with Ordered Inserts")
docs = [
    {"_id": 1, "title": "Ordered 1"},
    {"_id": 2, "title": "Ordered 2"},
    {"_id": 1, "title": "Duplicate ID"}
]
try:
    collection.insert_many(docs, ordered=True)
except BulkWriteError as bwe:
    print("BulkWriteError:")
    for err in bwe.details["writeErrors"]:
        pprint(err)

print("\n📌 Understanding the \"writeConcern\"")
coll_wc_majority = db.get_collection("tv_shows_wc", write_concern=WriteConcern("majority"))
coll_wc_majority.insert_one({"title": "WC Majority"})
pprint(coll_wc_majority.find_one({"title": "WC Majority"}))

print("\n📌 The \"writeConcern\" in Practice")
coll_wc_w1 = db.get_collection("tv_shows_wc", write_concern=WriteConcern(w=1))
coll_wc_w1.insert_one({"title": "WC w=1"})
for doc in coll_wc_w1.find({"title": {"$regex": "WC"}}):
    pprint(doc)

print("\n📌 What is Atomicity?")
collection.delete_many({})
collection.insert_one({
    "title": "Atomic Show",
    "details": {"runtime": 45, "genre": "Drama"}
})
collection.update_one(
    {"title": "Atomic Show"},
    {"$set": {"details.runtime": 50, "details.genre": "Mystery"}}
)
pprint(collection.find_one({"title": "Atomic Show"}))

print("\n📌 Time to Practice - Create Operations")
collection.delete_many({})
collection.insert_one({"title": "Solo Insert", "status": "active"})
collection.insert_many([
    {"title": "Multi Insert 1", "status": "archived"},
    {"title": "Multi Insert 2", "status": "pending"}
])
for doc in collection.find():
    pprint(doc)

print("\n📌 Importing Data")
with open("08. tv-shows.json", "r", encoding="utf-8") as file:
    data = json.load(file)
collection.delete_many({})
collection.insert_many(data)
print("Number of shows inserted:", collection.count_documents({}))
pprint(collection.find_one())

print("\n📌 Wrap Up")
print("You have seen insert_one, insert_many, ordered inserts, writeConcern, and atomic updates")

print("\n📌 Useful Resources & Links")
print("https://www.mongodb.com/docs/manual/core/crud-write-operations/")

collection.drop()
client.close()