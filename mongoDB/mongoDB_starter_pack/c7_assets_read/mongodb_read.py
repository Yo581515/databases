# tvshows_queries.py

from pymongo import MongoClient, ASCENDING, DESCENDING
from pprint import pprint


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["entertainment"]
collection = db["tvshows"]

# empty the collection (optional, for clean re-runs)
collection.delete_many({})


tv_shows_json = "02. tv-shows.json"
# Load the JSON data into the collection
import json
with open(tv_shows_json, "r") as file:
    data = json.load(file)
    collection.insert_many(data)

# 1. Basic findOne and find
print("🔍 Find one show:")
pprint(collection.find_one())
print()

print("\n🔍 All shows with language English:")
for show in collection.find({"language": "English"}):
    pprint(show)
    print()

# 2. Comparison Operators
print("\n🎯 Shows with rating > 8.5:")
for show in collection.find({"rating.average": {"$gt": 8.5}}):
    pprint(show)
    print()

# 3. Embedded Documents & Arrays
print("\n📆 Shows airing on Sunday:")
for show in collection.find({"schedule.days": "Sunday"}):
    pprint(show)
    print()

# 4. $in and $nin
print("\n🎭 Shows with Drama or Horror genres:")
for show in collection.find({"genres": {"$in": ["Drama", "Horror"]}}):
    pprint(show)
    print()

print("\n🚫 Shows NOT in Comedy or Music genres:")
for show in collection.find({"genres": {"$nin": ["Comedy", "Music"]}}):
    pprint(show)
    print()

# 5. Logical Operators: $or, $nor, $and, $not
print("\n⚖️ Shows that are either on HBO or have > 90 weight:")
query = {
    "$or": [
        {"network.name": "HBO"},
        {"weight": {"$gt": 90}}
    ]
}
for show in collection.find(query):
    pprint(show)
    print()

print("\n🚫 Shows NOT on FX or with < 8.0 rating:")
query = {
    "$nor": [
        {"network.name": "FX"},
        {"rating.average": {"$lt": 8.0}}
    ]
}
for show in collection.find(query):
    pprint(show)
    print()

print("\n✔️ Shows that are on FX AND have average rating > 8.0:")
query = {
    "$and": [
        {"network.name": "FX"},
        {"rating.average": {"$gt": 8.0}}
    ]
}
for show in collection.find(query):
    pprint(show)
    print()

print("\n❌ Shows that DO NOT have 'Running' status:")
for show in collection.find({"status": {"$not": {"$eq": "Running"}}}):
    pprint(show)
    print()

# 6. Element Operators
print("\n🔎 Shows where 'webChannel' field exists:")
for show in collection.find({"webChannel": {"$exists": True}}):
    pprint(show)
    print()

print("\n🧪 Shows where 'runtime' is a number:")
for show in collection.find({"runtime": {"$type": "int"}}):
    pprint(show)
    print()

# 7. Evaluation Operators
print("\n🔤 Shows with names starting with 'S':")
for show in collection.find({"name": {"$regex": "^S"}}):
    pprint(show)
    print()

print("\n📊 Using $expr: rating.average > weight / 10:")
for show in collection.find({
    "$expr": {"$gt": ["$rating.average", {"$divide": ["$weight", 10]}]}
}):
    pprint(show)
    print()

# 8. Array Query Selectors
print("\n📦 Shows that have exactly 3 genres:")
for show in collection.find({"genres": {"$size": 3}}):
    pprint(show)
    print()

print("\n🎯 Shows with ALL genres: Drama and Crime:")
for show in collection.find({"genres": {"$all": ["Drama", "Crime"]}}):
    pprint(show)
    print()

print("\n🎯 Shows where any genre is Horror and ends with 'e':")
for show in collection.find({"genres": {"$elemMatch": {"$regex": "e$"}}}):
    pprint(show)
    print()

# 9. Cursor Handling: sort, skip, limit
print("\n⬇️ First 3 shows sorted by rating descending:")
for show in collection.find().sort("rating.average", DESCENDING).limit(3):
    pprint(show)
    print()

print("\n➡️ Skip 2 and limit 3 shows sorted by weight:")
for show in collection.find().sort("weight", DESCENDING).skip(2).limit(3):
    pprint(show)
    print()

# 10. Projection  
print("\n📃 Show names and genres only:")
for show in collection.find({}, {"_id": 0, "name": 1, "genres": 1}):
    pprint(show)
    print()

print("\n🎯 Show only first 2 genres:")
for show in collection.find({}, {"name": 1, "genres": {"$slice": 2}}):
    pprint(show)
    print()

for show in collection.find({}, {"name": 1, "genres": {"$slice": 2}}):
    pprint(show)
    print()
