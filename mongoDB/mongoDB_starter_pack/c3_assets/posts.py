from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.schema_demo
client.drop_database("schema_demo")  # Resetting the DB

# -------------------- Document Example & Schema --------------------
db.patients.insert_one({
    "firstName": "Josef",
    "lastName": "Fesaha",
    "age": 27,
    "history": [
        {"date": "2023-03-10", "condition": "Flu", "treatment": "Physical therapy"},
        {"date": "2024-05-10", "condition": "Azma", "treatment": "Inhaler"}
    ],
    "student": {"student_id": 1, "student_name": "Josef"}
})

# Remove a nested field
db.patients.update_one(
    {"firstName": "Josef"},
    {"$unset": {"student.student_name": ""}}
)

# -------------------- Relationships --------------------

# One-to-One Embedded
db.users.insert_one({
    "username": "alice",
    "profile": {"bio": "Data scientist", "location": "Berlin"}
})

# One-to-One Reference
profile_id = db.profiles.insert_one({
    "bio": "ML engineer",
    "location": "NYC"
}).inserted_id
db.users_ref.insert_one({
    "username": "bob",
    "profile_id": profile_id
})

# One-to-Many Embedded
db.posts.insert_one({
    "title": "MongoDB Basics",
    "comments": [
        {"text": "Great post!", "author": "user1"},
        {"text": "Thanks!", "author": "user2"}
    ]
})

# One-to-Many Referenced
comment_ids = db.comments.insert_many([
    {"text": "Nice!", "author": "user1"},
    {"text": "Helpful!", "author": "user2"}
]).inserted_ids
db.posts_ref.insert_one({
    "title": "MongoDB Relationships",
    "comment_ids": comment_ids
})

# Many-to-Many Embedded
db.courses.insert_one({
    "name": "MongoDB Advanced",
    "students": [{"name": "Max"}, {"name": "Anna"}]
})

# Many-to-Many Referenced
student_ids = db.students.insert_many([
    {"name": "John"},
    {"name": "Emma"}
]).inserted_ids
db.courses_ref.insert_one({
    "name": "Data Modeling",
    "student_ids": student_ids
})

# -------------------- Using $lookup --------------------
print("\n🔍 Lookup Example (post_ref + comments):")
lookup_result = db.posts_ref.aggregate([
    {
        "$lookup": {
            "from": "comments",
            "localField": "comment_ids",
            "foreignField": "_id",
            "as": "comments_detail"
        }
    }
])
for doc in lookup_result:
    pprint(doc)

# -------------------- Schema Validation --------------------
print("\n🧪 Creating schema validation collection...")
db.create_collection("validated_users", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "email"],
        "properties": {
            "username": {"bsonType": "string"},
            "email": {"bsonType": "string", "pattern": "^.+@.+$"}
        }
    }
})

# Valid document
db.validated_users.insert_one({
    "username": "lucy",
    "email": "lucy@example.com"
})

# Invalid document (will fail unless validationAction is warn)
try:
    db.validated_users.insert_one({"username": "no_email"})
except Exception as e:
    print("❌ Validation failed:", e)

# Wrap up
print("\n✅ All schema and relation sections covered.")

'''# drop the database to clean up
client.drop_database("schema_demo")
# Close the MongoDB connection
client.close()
# End of the script
print("MongoDB connection closed.")
# End of the script'''