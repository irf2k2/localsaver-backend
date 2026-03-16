from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["localsaver"]

# Cities
cities = [
    {"name": "Dubai"},
    {"name": "Abu Dhabi"},
    {"name": "Sharjah"}
]

# Categories
categories = [
    {"name": "Restaurants"},
    {"name": "Cafes"},
    {"name": "Salons"},
    {"name": "Gyms"}
]

# Insert cities
if db.cities.count_documents({}) == 0:
    db.cities.insert_many(cities)
    print("Cities inserted")

# Insert categories
if db.categories.count_documents({}) == 0:
    db.categories.insert_many(categories)
    print("Categories inserted")

print("Database seeded successfully")