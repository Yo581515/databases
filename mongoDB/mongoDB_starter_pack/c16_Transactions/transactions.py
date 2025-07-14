from pymongo import MongoClient
from pymongo.errors import OperationFailure
from pprint import pprint

print("\n📌 Module Introduction")
print("MongoDB Transactions: ensure atomicity across multiple operations.\n")

print("\n📌 What are Transactions?")
print("Transactions group multiple read and write operations into a single atomic operation.\n")

print("\n📌 A Typical Usecase")
print("Example: Transferring funds between bank accounts — debit from one, credit to another.\n")

client = MongoClient("mongodb://localhost:27017/")
db = client["bank_demo"]
accounts = db["accounts"]
accounts.drop()

accounts.insert_many([
    {"name": "Alice", "balance": 1000},
    {"name": "Bob", "balance": 500}
])
print("📌 Initial Balances:")
for doc in accounts.find():
    pprint(doc)
print()

print("\n📌 How Does a Transaction Work?")
session = client.start_session()
try:
    with session.start_transaction():
        print("⏳ Starting transaction...")
        accounts.update_one({"name": "Alice"}, {"$inc": {"balance": -200}}, session=session)
        accounts.update_one({"name": "Bob"}, {"$inc": {"balance": 200}}, session=session)
        print("✅ Transaction committed.\n")
except OperationFailure as e:
    print("❌ Transaction aborted due to error:", e)
    session.abort_transaction()
finally:
    session.end_session()

print("📌 Final Balances:")
for doc in accounts.find():
    pprint(doc)
print()

print("\n📌 Useful Resources & Links")
print("https://www.mongodb.com/docs/manual/core/transactions/")