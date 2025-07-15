from pymongo import MongoClient
from datetime import datetime
from datetime import UTC

# 1. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["game_database"]
collection = db["characters"]

# 2. Insert Documents
characters = [
    {
        "name": "Archer",
        "class": "Ranger",
        "level": 12,
        "skills": ["Bow Mastery", "Stealth"],
        "created_at": datetime.now(UTC)
    },
    {
        "name": "Mage",
        "class": "Sorcerer",
        "level": 18,
        "skills": ["Fireball", "Teleport"],
        "created_at": datetime.now(UTC)
    },
    {
        "name": "Knight",
        "class": "Warrior",
        "level": 10,
        "skills": ["Shield Block", "Charge"],
        "created_at": datetime.now(UTC)
    }
]

# Insert many
collection.insert_many(characters)

# 3. Find Documents (Basic Query)
print("\nAll characters:")
for char in collection.find():
    print(char)

# 4. Using Cursors with Filters
print("\nCharacters above level 10:")
cursor = collection.find({"level": {"$gt": 10}})
for char in cursor:
    print(char)

# 5. Update Documents
print("\nUpdating Mage's level to 20:")
collection.update_one({"name": "Mage"}, {"$set": {"level": 20}})

# 6. Delete Documents
print("\nDeleting Knight:")
collection.delete_one({"name": "Knight"})

# 7. Using Operators
print("\nCharacters with level >= 12:")
for char in collection.find({"level": {"$gte": 12}}):
    print(char)

# 8. Working with Dates
print("\nCharacters created in the last hour:")
one_hour_ago = datetime.now(UTC)
for char in collection.find({"created_at": {"$lte": one_hour_ago}}):
    print(char)

# 9. Working with Arrays
print("\nCharacters with 'Fireball' skill:")
for char in collection.find({"skills": "Fireball"}):
    print(char)

# 10. Clean MongoDB Class Example
class GameDB:
    def __init__(self, db_name="game_database", collection_name="characters"):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_character(self, char_data):
        self.collection.insert_one(char_data)

    def find_by_level(self, min_level):
        return list(self.collection.find({"level": {"$gte": min_level}}))

    def update_character(self, name, updates):
        self.collection.update_one({"name": name}, {"$set": updates})

    def delete_character(self, name):
        self.collection.delete_one({"name": name})

# 11. Usage of Clean Class
print("\nUsing GameDB class:")
game_db = GameDB()
game_db.insert_character({
    "name": "Rogue",
    "class": "Assassin",
    "level": 15,
    "skills": ["Backstab", "Vanish"],
    "created_at": datetime.utcnow()
})
high_levels = game_db.find_by_level(14)
for char in high_levels:
    print(char)