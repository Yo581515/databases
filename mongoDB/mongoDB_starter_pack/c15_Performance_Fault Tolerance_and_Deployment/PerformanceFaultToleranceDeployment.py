from pymongo import MongoClient
from pymongo.errors import OperationFailure
from pprint import pprint
import time

print("\n📌 Module Introduction")
print("This module explores performance, fault tolerance, and deployment in MongoDB.\n")

client = MongoClient("mongodb://localhost:27017/")
db = client["performance_demo"]

print("\n📌 What Influences Performance?")
print("Indexes, data schema design, hardware specs, queries, and server load all impact performance.\n")

print("\n📌 Understanding Capped Collections")
db.drop_collection("logs")
db.create_collection("logs", capped=True, size=1024 * 1024, max=5)
logs = db["logs"]

for i in range(7):
    logs.insert_one({"log_id": i, "event": f"Log entry #{i}", "ts": time.time()})
    time.sleep(0.2)

print("📌 Capped Collection Contents (max 5):")
for doc in logs.find():
    pprint(doc)
print()

print("\n📌 What are Replica Sets?")
print("Replica sets offer high availability via automatic failover and data replication.")
print("Note: Setup involves configuring mongod with --replSet and initializing it with rs.initiate().")
print("Not directly demoed in this script.\n")

print("\n📌 Understanding Sharding")
print("Sharding distributes data across multiple machines for horizontal scaling.")
print("Requires config servers, query routers (mongos), and sharded collections.")
print("Also not directly demoed in standalone scripts.\n")

print("\n📌 Deploying a MongoDB Server")
print("Run `mongod` with options such as `--dbpath`, `--port`, `--replSet`, or use Docker.")
print("Docker example:\n  docker run -d -p 27017:27017 --name mongo mongo\n")

print("\n📌 Using MongoDB Atlas")
print("1. Go to https://cloud.mongodb.com\n2. Create a free cluster\n3. Choose region, name, and provider\n4. Create database and user\n5. Connect with MongoClient URI\n")

print("\n📌 Backups & Setting Alerts in MongoDB Atlas")
print("- Backups: Enabled by default on Atlas.\n- Alerts: Set thresholds for disk, memory, replication lag, etc., in Alerts tab.\n")

print("\n📌 Connecting to our Cluster")
print("Example connection URI:\n")
print('MongoClient("mongodb+srv://<user>:<pass>@cluster0.mongodb.net/?retryWrites=true&w=majority")\n')

print("\n📌 Wrap Up")
print("We covered performance factors, replication, sharding, deployment options, and Atlas usage.\n")

print("\n📌 Useful Resources & Links")
print("https://www.mongodb.com/docs/manual/administration/")
print("https://www.mongodb.com/cloud/atlas")