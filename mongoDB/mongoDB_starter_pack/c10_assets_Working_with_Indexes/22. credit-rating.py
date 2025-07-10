from pymongo import MongoClient
import random

client = MongoClient("mongodb://localhost:27017/")
db = client["credit"]

for i in range(1000):
    db.ratings.insert_one({
        "person_id": i + 1,
        "score": random.random() * 100,
        "age": random.randint(18, 87)
    })
    

db.drop_collection("credit")    
client.close()
