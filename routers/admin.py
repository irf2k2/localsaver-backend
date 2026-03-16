from fastapi import APIRouter, HTTPException, Depends
from database import db
from passlib.context import CryptContext
from auth import create_access_token, get_current_admin
from bson import ObjectId

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/admin/login")
def admin_login(data: dict):

    admin = db.admins.find_one({"email": data["email"]})

    if not admin:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not pwd_context.verify(data["password"], admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({
        "admin_id": str(admin["_id"]),
        "role": "admin"
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
# ----------------------------
# Admin View Merchants
# ----------------------------

@router.get("/admin/merchants")
def get_merchants(admin=Depends(get_current_admin)):

    merchants = list(db.merchants.find())
    result = [] 

    for merchant in merchants:
        result.append({
            "_id": str(merchant["_id"]),
            "name": merchant.get("name"),
            "phone": merchant.get("phone"),
            "email": merchant.get("email"),
            "business_name": merchant.get("business_name"),
            "status": merchant.get("status", "active")
        })

    return result

# ----------------------------
# Admin Disable Merchant
# ----------------------------

@router.post("/admin/merchant/disable")
def disable_merchant(data: dict, admin=Depends(get_current_admin)):

    if "merchant_id" not in data:
        raise HTTPException(status_code=400, detail="merchant_id required")

    result = db.merchants.update_one(
        {"_id": ObjectId(data["merchant_id"])},
        {"$set": {"status": "disabled"}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Merchant not found")

    return {
        "message": "Merchant disabled successfully"
    }

# ----------------------------
# Admin View Users
# ----------------------------

@router.get("/admin/users")
def get_users(admin=Depends(get_current_admin)):

    users = list(db.users.find())
    result = []

    for user in users:
        result.append({
            "_id": str(user["_id"]),
            "name": user.get("name"),
            "phone": user.get("phone"),
            "status": user.get("status", "active")
        })

    return result


# ----------------------------
# Admin Disable User
# ----------------------------

@router.post("/admin/user/disable")
def disable_user(data: dict):

    if "user_id" not in data:
        raise HTTPException(status_code=400, detail="user_id required")

    result = db.users.update_one(
        {"_id": ObjectId(data["user_id"])},
        {"$set": {"status": "disabled"}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "message": "User disabled successfully"
    }

# ----------------------------
# Admin View Redemptions
# ----------------------------

@router.get("/admin/redemptions")
def get_redemptions():

    redemptions = list(db.redemptions.find())
    result = []

    for r in redemptions:
        result.append({
            "_id": str(r["_id"]),
            "deal_id": r.get("deal_id"),
            "store_id": r.get("store_id"),
            "user_id": r.get("user_id"),
            "redeemed_at": r.get("redeemed_at")
        })

    return result