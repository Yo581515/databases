from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient("mongodb://localhost:27017/")

try:
    client.admin.command('ping')
    print("MongoDB is running!")
except Exception as e:
    print("MongoDB is not running:", e)
    
try:
    client.drop_database("c12_agg_db")
    print("Database 'c12_agg_db' dropped successfully.")
except Exception as e:
    print("Error dropping database 'c12_agg_db':", e)

db = client["c12_agg_db"]
collection = db["persons"]

collection.delete_many({})

with open("03. persons.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    collection.insert_many(data)


collection_2 = db["students"]
collection_2.delete_many({})

with open("13. array-data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    collection_2.insert_many(data)
    
print("Data inserted successfully!")
