from pymongo import MongoClient
from pprint import pprint

print("\n📌 Module Introduction")

client = MongoClient("mongodb://localhost:27017/")
db = client["delete_demo_db"]
collection = db["shows"]
collection.drop()

collection.insert_many([
    {"title": "Show A", "genre": "Drama"},
    {"title": "Show B", "genre": "Horror"},
    {"title": "Show C", "genre": "Drama"},
    {"title": "Show D", "genre": "Comedy"}
])

print("\n📌 Understanding \"deleteOne()\" & \"deleteMany()\"")

collection.delete_one({"genre": "Drama"})
print("Deleted one document with genre Drama")

collection.delete_many({"genre": "Drama"})
print("Deleted all remaining documents with genre Drama")

print("Remaining documents:")
for doc in collection.find():
    pprint(doc)

print("\n📌 Deleting All Entries in a Collection")
collection.delete_many({})
print("All documents deleted")

print("Document count:", collection.count_documents({}))

print("\n📌 Useful Resources & Links")
print("https://www.mongodb.com/docs/manual/reference/method/db.collection.deleteOne/")
print("https://www.mongodb.com/docs/manual/reference/method/db.collection.deleteMany/")
