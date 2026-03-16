from fastapi import APIRouter, Query, Depends
from database import db
from auth import get_current_merchant

router = APIRouter()


# ----------------------------
# Get stores (optionally filter by city)
# Public API for mobile app
# ----------------------------
@router.get("/stores")
def get_stores(city: str = Query(None)):

    query = {}

    if city:
        query["city"] = city

    stores = list(db.stores.find(query))

    for store in stores:
        store["_id"] = str(store["_id"])

    return stores


# ----------------------------
# Admin creates store
# ----------------------------
@router.post("/admin/store")
def create_store(data: dict):

    store = {
        "merchant_id": data.get("merchant_id"),  # admin assigns store to merchant
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


# ----------------------------
# Merchant Dashboard - My Stores
# ----------------------------
@router.get("/merchant/stores")
def get_merchant_stores(merchant=Depends(get_current_merchant)):

    stores = list(db.stores.find({"merchant_id": merchant["merchant_id"]}))

    for store in stores:
        store["_id"] = str(store["_id"])

    return stores