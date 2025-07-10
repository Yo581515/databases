from pymongo import MongoClient, GEOSPHERE
from pprint import pprint

print("\n📌 Module Introduction")

client = MongoClient("mongodb://localhost:27017/")
db = client["geo_demo_db"]
places = db["places"]
places.drop()

print("\n📌 Adding GeoJSON Data")
places.insert_many([
    {
        "name": "Central Park",
        "location": {
            "type": "Point",
            "coordinates": [-73.9654, 40.7829]
        }
    },
    {
        "name": "Times Square",
        "location": {
            "type": "Point",
            "coordinates": [-73.9851, 40.7580]
        }
    },
    {
        "name": "Empire State Building",
        "location": {
            "type": "Point",
            "coordinates": [-73.9857, 40.7484]
        }
    }
])
print("Inserted initial GeoJSON locations.\n")

print("\n📌 Running Geo Queries (Before Index — should fail or be inefficient)")
try:
    cursor = places.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [-73.9851, 40.7580]
                }
            }
        }
    })
    for doc in cursor:
        pprint(doc)
        print()
except Exception as e:
    print("Geo query failed (no index yet):", e)
print()

print("\n📌 Adding a Geospatial Index to Track the Distance")
places.create_index([("location", GEOSPHERE)])
print("Geospatial index created.\n")

print("\n📌 Running Geo Queries (Now should work)")
cursor = places.find({
    "location": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": [-73.9851, 40.7580]
            }
        }
    }
})
for doc in cursor:
    pprint(doc)
    print()

print("\n📌 Adding Additional Locations")
places.insert_many([
    {
        "name": "Brooklyn Bridge",
        "location": {
            "type": "Point",
            "coordinates": [-73.9969, 40.7061]
        }
    },
    {
        "name": "Statue of Liberty",
        "location": {
            "type": "Point",
            "coordinates": [-74.0445, 40.6892]
        }
    }
])
print("Added Brooklyn Bridge and Statue of Liberty.\n")

print("\n📌 Finding Places Inside a Certain Area")
polygon = {
    "type": "Polygon",
    "coordinates": [[
        [-74.02, 40.70],
        [-73.97, 40.70],
        [-73.97, 40.75],
        [-74.02, 40.75],
        [-74.02, 40.70]
    ]]
}
cursor = places.find({
    "location": {
        "$geoWithin": {
            "$geometry": polygon
        }
    }
})
for doc in cursor:
    pprint(doc)
    print()


####
print("\n📌 Finding Out If a User Is Inside a Specific Area")
areas = db["areas"]
areas.drop()
# Insert Golden Gate Park polygon
areas.insert_one({
    "name": "Golden Gate Park",
    "area": {
        "type": "Polygon",
        "coordinates": [[
            [-122.4547, 37.77473],
            [-122.45303, 37.76641],
            [-122.51026, 37.76411],
            [-122.51026, 37.77473], 
            [-122.4547, 37.77473]
        ]]
    }
})
areas.create_index([("area", GEOSPHERE)])
print("Inserted area for Golden Gate Park.\n")
user_location = {
    "type": "Point",
    "coordinates": [-122.49089, 37.76992]
}
result = areas.find_one({
    "area": {
        "$geoIntersects": {
            "$geometry": user_location
        }
    }
})
if result:
    print("✅ User is inside:", result["name"])
else:
    print("❌ User is not inside any known area.")
areas.drop()
print()


print("\n📌 Finding Places Within a Certain Radius (1km from Times Square using $centerSphere)")
# Earth's radius = ~6378.1 km
km_radius = 1
radians = km_radius / 6378.1  # Convert 1km to radians
cursor = places.find({
    "location": {
        "$geoWithin": {
            "$centerSphere": [[-73.9851, 40.7580], radians]
        }
    }
})
for doc in cursor:
    pprint(doc)
    print()


print("\n📌 Useful Resources & Links")
print("https://www.mongodb.com/docs/manual/geospatial-queries/")

places.drop()
client.close()