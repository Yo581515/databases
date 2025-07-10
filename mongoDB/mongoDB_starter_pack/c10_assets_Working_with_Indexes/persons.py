from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["contacts_db"]
collection = db["persons"]

collection.delete_many({})

with open("03. persons.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    collection.insert_many(data)


collection.drop()
client.close()