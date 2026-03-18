from fastapi import APIRouter, HTTPException
from datetime import datetime
from database import db

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)


# 🔹 1. Get Wallet Balance
@router.get("/{user_id}")
def get_wallet(user_id: str):
    wallet = db.wallet.find_one({"user_id": user_id})

    if not wallet:
        return {
            "user_id": user_id,
            "points": 0,
            "wallet_value": 0
        }

    points = wallet.get("points", 0)

    return {
        "user_id": user_id,
        "points": points,
        "wallet_value": points * 0.25  # 💰 conversion
    }


# 🔹 2. Request Withdraw
@router.post("/withdraw")
def request_withdraw(data: dict):
    user_id = data.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="user_id required")

    wallet = db.wallet.find_one({"user_id": user_id})

    if not wallet or wallet.get("points", 0) < 100:
        raise HTTPException(
            status_code=400,
            detail="Minimum 100 points required"
        )

    points = wallet["points"]
    amount = points * 0.25

    # 🔹 Save withdraw request
    db.withdraw_requests.insert_one({
        "user_id": user_id,
        "points": points,
        "amount": amount,
        "status": "pending",
        "created_at": datetime.utcnow()
    })

    # 🔹 Reset wallet
    db.wallet.update_one(
        {"user_id": user_id},
        {"$set": {"points": 0}}
    )

    return {
        "message": "Withdraw request submitted",
        "points": points,
        "amount": amount
    }