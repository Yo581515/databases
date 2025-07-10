# users_update_queries.py

from pymongo import MongoClient
from pprint import pprint
import json

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["userdb"]
collection = db["users"]

# Optional: Clean slate
collection.delete_many({})

# Load data
with open("02. users.json", "r") as file:
    data = json.load(file)
    collection.insert_many(data)

print("\n📌 1. Set age = 35 for user named Max")
collection.update_one({"name": "Max"}, {"$set": {"age": 35}})
pprint(collection.find_one({"name": "Max"}))
print()

print("\n📌 2. Set verified = False for all users")
collection.update_many({}, {"$set": {"verified": False}})
for user in collection.find():
    pprint(user)
    print()

print("\n📌 3. Set isAdmin=True and country='USA' for Manuel")
collection.update_one({"name": "Manuel"}, {"$set": {"isAdmin": True, "country": "USA"}})
pprint(collection.find_one({"name": "Manuel"}))
print()

print("\n📌 4. Increment age by 1 for all users with age field")
collection.update_many({"age": {"$exists": True, "$ne": None}}, {"$inc": {"age": 1}})
for user in collection.find({"age": {"$exists": True}}):
    pprint(user)
    print()

print("\n📌 5. Use $min to keep smaller phone number for Anna")
collection.update_one({"name": "Anna"}, {"$min": {"phone": 500000000}})
pprint(collection.find_one({"name": "Anna"}))
print()

print("\n📌 6. Multiply age by 2 for Manuel")
collection.update_one({"name": "Manuel"}, {"$mul": {"age": 2}})
pprint(collection.find_one({"name": "Manuel"}))
print()

print("\n📌 7. Remove isAdmin from all users")
collection.update_many({}, {"$unset": {"isAdmin": ""}})
for user in collection.find():
    pprint(user)
    print()

print("\n📌 8. Rename 'phone' to 'phoneNumber'")
collection.update_many({}, {"$rename": {"phone": "phoneNumber"}})
for user in collection.find():
    pprint(user)
    print()

print("\n📌 9. Upsert user named 'Tony'")
collection.update_one({"name": "Tony"}, {"$set": {"age": 40}}, upsert=True)
pprint(collection.find_one({"name": "Tony"}))
print()

print("\n📌 10. Update 'highFrequency' to True for 'Sports' hobbies with frequency >= 3")
collection.update_many(
    {
        "hobbies": {
            "$elemMatch": {
                "title": "Sports",
                "frequency": {"$gte": 3}
            }
        }
    },
    {"$set": {"hobbies.$.highFrequency": True}}
)
for user in collection.find({"hobbies": {"$elemMatch": {"title": "Sports", "highFrequency": True}}}):
    pprint(user)
    print()

print("\n📌 11. Multiply all 'frequency' fields by 2")
collection.update_many(
    {"age": {"$gt": 30 }, "hobbies": {"$type": "array"}},
    {"$set": {"hobbies.$[].frequency": {"$multiply": ["$hobbies.frequency", 2]}}}
)
for user in collection.find({"age": {"$gt": 30 }}):
    pprint(user)
    print()

print("\n📌 12. Finding and updating specific fields")
collection.update_many({ "hobbies.frequency": {"$gt": 2}},
                       {"$set" : {"hobbies.$[elem].goodFrequency": True}},
                       array_filters=[{"elem.frequency": {"$gt": 2}}])
for user in collection.find({"hobbies": {"$elemMatch": {"goodFrequency": True}}}):
    pprint(user)
    print()
    

print("\n📌 13. Add 'Cooking' hobby to all Anna")
collection.update_many({"name": "Anna"}, {"$push": {"hobbies": {"title": "Cooking", "frequency": 1}}})
for user in collection.find({"name": "Anna", "hobbies": {"$exists": True}}):
    pprint(user)
    print()


print("\n📌 14. Remove all hobbies with title='Cooking'") # last item pop, 1 , -1
collection.update_many({}, {"$pull": {"hobbies": {"title": "Cooking"}}})
for user in collection.find({"hobbies": {"$exists": True}}):
    pprint(user)
    print()
    

print("\n📌 15. Add 'Reading' hobby only if not present for Anna")
collection.update_one({"name": "Anna"}, {"$addToSet": {"hobbies": {"title": "Reading", "frequency": 2}}})
pprint(collection.find_one({"name": "Anna"}))
print()


collection.drop()
client.close()