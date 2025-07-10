from pymongo import MongoClient
from pprint import pprint
import json

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Access the database and collection
db = client.flights
passengers = db.passengers

# Clear collection (optional, for clean re-runs)
passengers.delete_many({})

# Read JSON file
with open("12. 02-passengers.json", "r") as file:
    passengers_json = json.load(file)

# Insert the dataset
passengers.insert_many(passengers_json)

# Basic CRUD operations
passengers.insert_one({ "name": "Emily", "age": 29 })
pprint(passengers.find_one({ "age": 29 }))

passengers.update_one({ "name": "Emily" }, { "$set": { "age": 30 } })
passengers.delete_one({ "name": "Emily" })

# insertMany example
passengers.insert_many([
    { "name": "Person A", "age": 22 },
    { "name": "Person B", "age": 33 },
    { "name": "Person C", "age": 44 }
])

# Query: age > 30
print("\nPassengers with age > 30:")
for doc in passengers.find({ "age": { "$gt": 30 } }):
    pprint(doc)

# update vs updateMany
passengers.update_one({ "age": 30 }, { "$set": { "age": 31 } })
passengers.update_many({ "age": 35 }, { "$set": { "senior": True } })

# Projection
print("\nNames of all passengers:")
for doc in passengers.find({}, { "name": 1, "_id": 0 }):
    pprint(doc)

# Embedded document
passengers.insert_one({
    "name": "Emily",
    "age": 25,
    "address": {
        "city": "New York",
        "zip": "10001"
    }
})

# Query embedded document
print("\nPassenger from New York:")
pprint(passengers.find_one({ "address.city": "New York" }))

# Array example
passengers.update_one(
    { "name": "Emily" },
    { "$set": { "hobbies": ["reading", "yoga", "coding"] } }
)

# Query array field
print("\nPassenger who likes coding:")
pprint(passengers.find_one({ "hobbies": "coding" }))

# Access nested field projection
print("\nName and city for passenger with zip 10001:")
result = passengers.find_one(
    { "address.zip": "10001" },
    { "name": 1, "address.city": 1, "_id": 0 }
)
pprint(result)

db.drop_collection("passengers")
# Close the MongoDB connection
client.close()