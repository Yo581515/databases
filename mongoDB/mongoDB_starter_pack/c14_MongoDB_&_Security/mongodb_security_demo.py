from pymongo import MongoClient
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError
from pprint import pprint

print("\n📌 Module Introduction")
print("MongoDB Security: Covers authentication, authorization, and encryption.\n")

# Admin client (no auth or root user assumed)
admin_client = MongoClient("mongodb://localhost:27017/")
admin_db = admin_client["admin"]


# delete existing user if exists
print("📌 Dropping Existing User")
try:
    admin_db.command("dropUser", "testUser")
    print("Existing user 'testUser' dropped.\n")
except OperationFailure as e:
    if "no such user" in str(e):
        print("No existing user 'testUser' to drop.\n")
    else:
        print("Error dropping user:", e)
        
# delete secure_demo database if exists
print("\n📌 Dropping Existing Database")
try:
    secure_db = admin_client["secure_demo"]
    secure_db.command("dropDatabase")
    print("Existing database 'secure_demo' dropped.\n")
except OperationFailure as e:
    if "not found" in str(e):
        print("No existing database 'secure_demo' to drop.\n")
    else:
        print("Error dropping database:", e)
        
# delete test database if exists
print("\n📌 Dropping Existing Database")
try:
    test_db = admin_client["test"]
    test_db.command("dropDatabase")
    print("Existing database 'test' dropped.\n")
except OperationFailure as e:
    if "not found" in str(e):
        print("No existing database 'test' to drop.\n")
    else:
        print("Error dropping database:", e)

print("\n📌 Creating a User")
try:
    admin_db.command("createUser", "testUser", pwd="password123", roles=[{"role": "readWrite", "db": "secure_demo"}])
    print("User 'testUser' created.\n")
except OperationFailure as e:
    print("User creation error:", e)

print("\n📌 Updating & Extending Roles to Other Databases")
try:
    admin_db.command("updateUser", "testUser", roles=[
        {"role": "readWrite", "db": "secure_demo"},
        {"role": "read", "db": "test"}
    ])
    print("Roles updated for user 'testUser'.\n")
except OperationFailure as e:
    print("Role update error:", e)

print("\n📌 Connecting with Authenticated User and db:secure_demo : read and write permission")
try:
    user_client = MongoClient("mongodb://testUser:password123@localhost:27017/?authSource=admin")
    db = user_client["secure_demo"]
    collection = db["secure_collection"]
    collection.drop()

    print("Connected as 'testUser' to 'secure_demo'.\n")

    print("📌 INSERT")
    collection.insert_one({"name": "Alice", "role": "analyst"})
    print("Inserted document.\n")

    print("📌 READ")
    doc = collection.find_one({"name": "Alice"})
    pprint(doc)
    print()

    print("📌 UPDATE")
    collection.update_one({"name": "Alice"}, {"$set": {"role": "senior analyst"}})
    updated_doc = collection.find_one({"name": "Alice"})
    pprint(updated_doc)
    print()

    print("📌 DELETE")
    collection.delete_one({"name": "Alice"})
    deleted = collection.find_one({"name": "Alice"})
    print("Deleted successfully." if not deleted else "Delete failed.")
    print()

except ServerSelectionTimeoutError as e:
    print("Connection error:", e)
except OperationFailure as e:
    print("Auth or permission error:", e)
    
    
    
print("\n📌 Connecting with Authenticated User and db:test : only read permission")
try:
    user_client = MongoClient("mongodb://testUser:password123@localhost:27017/?authSource=admin")
    db = user_client["test"]
    collection = db["secure_collection"]
    collection.drop()

    print("Connected as 'testUser' to 'secure_demo'.\n")

    print("📌 INSERT")
    collection.insert_one({"name": "Alice", "role": "analyst"})
    print("Inserted document.\n")

    print("📌 READ")
    doc = collection.find_one({"name": "Alice"})
    pprint(doc)
    print()

    print("📌 UPDATE")
    collection.update_one({"name": "Alice"}, {"$set": {"role": "senior analyst"}})
    updated_doc = collection.find_one({"name": "Alice"})
    pprint(updated_doc)
    print()

    print("📌 DELETE")
    collection.delete_one({"name": "Alice"})
    deleted = collection.find_one({"name": "Alice"})
    print("Deleted successfully." if not deleted else "Delete failed.")
    print()

except ServerSelectionTimeoutError as e:
    print("Connection error:", e)
except OperationFailure as e:
    print("Auth or permission error:", e)
    
    
    

print("\n📌 Adding SSL Transport Encryption")
print("Enable TLS in MongoDB with `--tlsMode requireTLS --tlsCertificateKeyFile`.")
print("Client example:\nMongoClient(..., tls=True, tlsCertificateKeyFile='client.pem')\n")

print("\n📌 Encryption at REST")
print("Enable Encrypted Storage Engine using `--enableEncryption --encryptionKeyFile`.\n")

print("\n📌 Wrap Up")
print("You now understand users, roles, CRUD, and encryption strategies in MongoDB.\n")

print("\n📌 Useful Resources & Links")
print("https://www.mongodb.com/docs/manual/core/authorization/")
print("https://www.mongodb.com/docs/manual/core/security-encryption/")