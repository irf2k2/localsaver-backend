from fastapi import APIRouter, Query, Depends
from database import db
from auth import get_current_merchant

router = APIRouter()


# ----------------------------
# Get deals (optionally filter by city)
# ----------------------------
@router.get("/deals")
def get_deals(city: str = Query(None)):

    query = {}

    if city:
        query["city"] = city

    deals = list(db.deals.find(query))

    for deal in deals:
        deal["_id"] = str(deal["_id"])

    return deals


# ----------------------------
# Create deal (Merchant only)
# ----------------------------
@router.post("/merchant/deal")
def create_deal(data: dict, merchant=Depends(get_current_merchant)):

    deal = {
        "merchant_id": merchant["merchant_id"],   # automatically attach merchant
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

# ----------------------------
# Get deals for specific store
# ----------------------------
@router.get("/store/{store_id}/deals")
def get_store_deals(store_id: str):

    deals = list(db.deals.find({"store_id": store_id}))

    for deal in deals:
        deal["_id"] = str(deal["_id"])

    return deals
# ----------------------------
# Merchant Dashboard - View My Deals
# ----------------------------
@router.get("/merchant/deals")
def get_merchant_deals(merchant=Depends(get_current_merchant)):

    deals = list(db.deals.find({"merchant_id": merchant["merchant_id"]}))

    for deal in deals:
        deal["_id"] = str(deal["_id"])

    return deals

# ----------------------------
# Merchant Dashboard Summary
# ----------------------------
@router.get("/merchant/dashboard")
def merchant_dashboard(merchant=Depends(get_current_merchant)):

    merchant_id = merchant["merchant_id"]

    total_stores = db.stores.count_documents({"merchant_id": merchant_id})

    total_deals = db.deals.count_documents({"merchant_id": merchant_id})

    active_deals = db.deals.count_documents({
        "merchant_id": merchant_id
    })

    total_redemptions = db.redemptions.count_documents({
        "merchant_id": merchant_id
    })

    return {
        "total_stores": total_stores,
        "total_deals": total_deals,
        "active_deals": active_deals,
        "total_redemptions": total_redemptions
    }
