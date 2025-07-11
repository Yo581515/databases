from pymongo import MongoClient
from bson.decimal128 import Decimal128
from bson.int64 import Int64
from pprint import pprint
import decimal

print("\n📌 Module Introduction")

client = MongoClient("mongodb://localhost:27017/")
db = client["numerical_demo"]
collection = db["numbers"]
collection.drop()

print("\n📌 Number Types - An Overview")
doc = {
    "int32_example": 42,
    "int64_example": Int64(9223372036854775807),
    "float_example": 3.14159,
    "decimal128_example": Decimal128("1234567890.12345678901234567890")
}
collection.insert_one(doc)
pprint(collection.find_one()); print()

print("\n📌 MongoDB Shell & Data Types")
print("Types stored as BSON: int32, int64, double, decimal128"); print()

print("\n📌 Understanding Programming Language Defaults")
print("Python defaults to int (arbitrary precision) and float (64-bit double)"); print()

print("\n📌 Working with int32")
collection.insert_one({"num": 2147483647})
pprint(collection.find_one({"num": 2147483647})); print()

print("\n📌 Working with int64")
collection.insert_one({"num": Int64(9223372036854775807)})
pprint(collection.find_one({"num": Int64(9223372036854775807)})); print()

print("\n📌 Doing Maths with Floats, int32s & int64s")
collection.drop()  # Clear collection for fresh start
doc = {
    "int32": 10,
    "int64": Int64(20),
    "float": 2.5
}
collection.insert_one(doc)
res = collection.aggregate([
    {
        "$project": {
            "_id": 0,
            "sum": {"$add": ["$int32", "$int64", "$float"]},
            "avg": {"$avg": ["$int32", "$int64", "$float"]}
        }
    }
])
for doc in res:
    pprint(doc)
    print()

print("\n📌 What's Wrong with Normal Doubles?")
collection.insert_one({"bad_float_math": 0.1 + 0.2})
pprint(collection.find_one({"bad_float_math": {"$exists": True}})); print()

print("\n📌 Working with Decimal 128bit")
decimal.getcontext().prec = 30
precise_sum = Decimal128(str(decimal.Decimal("0.1") + decimal.Decimal("0.2")))
collection.insert_one({"precise_decimal_sum": precise_sum})
pprint(collection.find_one({"precise_decimal_sum": {"$exists": True}})); print()

print("\n📌 Useful Resources & Links")
print("https://www.mongodb.com/docs/manual/reference/bson-types/")

collection.drop()
client.close()