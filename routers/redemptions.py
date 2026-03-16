from fastapi import APIRouter, Depends
from database import db
from datetime import datetime
from auth import get_current_merchant

router = APIRouter()


# ----------------------------
# Redeem a deal
# ----------------------------
@router.post("/redeem-deal")
def redeem_deal(data: dict):

    # Find the deal to get merchant_id
    deal = db.deals.find_one({"_id": data["deal_id"]})

    redemption = {
        "deal_id": data["deal_id"],
        "store_id": data["store_id"],
        "user_id": data["user_id"],
        "merchant_id": deal.get("merchant_id") if deal else None,
        "redeemed_at": datetime.utcnow()
    }

    result = db.redemptions.insert_one(redemption)

    return {
        "message": "Deal redeemed successfully",
        "redemption_id": str(result.inserted_id)
    }


# ----------------------------
# Merchant Dashboard - View Redemptions
# ----------------------------
@router.get("/merchant/redemptions")
def get_merchant_redemptions(merchant=Depends(get_current_merchant)):

    redemptions = list(db.redemptions.find({"merchant_id": merchant["merchant_id"]}))

    for r in redemptions:
        r["_id"] = str(r["_id"])

    return redemptions