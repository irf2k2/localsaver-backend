from fastapi import APIRouter, Query
from database import db

router = APIRouter()


# Get deals (optionally filter by city)
@router.get("/deals")
def get_deals(city: str = Query(None)):

    query = {}

    if city:
        query["city"] = city

    deals = list(db.deals.find(query))

    for deal in deals:
        deal["_id"] = str(deal["_id"])

    return deals


# Create deal
@router.post("/merchant/deal")
def create_deal(data: dict):

    deal = {
        "store_id": data["store_id"],
        "city": data["city"],
        "title": data["title"],
        "description": data["description"],
        "discount": data["discount"],
        "start_date": data["start_date"],
        "end_date": data["end_date"]
    }

    result = db.deals.insert_one(deal)

    return {
        "message": "Deal created",
        "deal_id": str(result.inserted_id)
    }
#----------------- Get deals for specific store
@router.get("/store/{store_id}/deals")
def get_store_deals(store_id: str):

    deals = list(db.deals.find({"store_id": store_id}))

    for deal in deals:
        deal["_id"] = str(deal["_id"])

    return deals