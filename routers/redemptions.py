from fastapi import APIRouter
from database import db
from datetime import datetime

router = APIRouter()


# Redeem a deal
@router.post("/redeem-deal")
def redeem_deal(data: dict):

    redemption = {
        "deal_id": data["deal_id"],
        "store_id": data["store_id"],
        "user_id": data["user_id"],
        "redeemed_at": datetime.utcnow()
    }

    result = db.redemptions.insert_one(redemption)

    return {
        "message": "Deal redeemed successfully",
        "redemption_id": str(result.inserted_id)
    }