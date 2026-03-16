from fastapi import APIRouter, Query
from database import db

router = APIRouter()


# Get stores (optionally filter by city)
@router.get("/stores")
def get_stores(city: str = Query(None)):

    query = {}

    if city:
        query["city"] = city

    stores = list(db.stores.find(query))

    for store in stores:
        store["_id"] = str(store["_id"])

    return stores


# Admin creates store
@router.post("/admin/store")
def create_store(data: dict):

    store = {
        "store_name": data["store_name"],
        "category": data["category"],
        "city": data["city"],
        "address": data["address"],
        "latitude": data["latitude"],
        "longitude": data["longitude"]
    }

    result = db.stores.insert_one(store)

    return {
        "message": "Store created",
        "store_id": str(result.inserted_id)
    }