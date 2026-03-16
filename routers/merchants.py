from fastapi import APIRouter
from database import db
from auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/merchants/register")
def register_merchant(data: dict):

    data["password"] = hash_password(data["password"])
    data["status"] = "active"

    result = db.merchants.insert_one(data)

    return {
        "message": "Merchant registered",
        "merchant_id": str(result.inserted_id)
    }


@router.post("/merchants/login")
def login_merchant(data: dict):

    if "email" not in data or "password" not in data:
        return {"error": "Email and password required"}

    merchant = db.merchants.find_one({"email": data["email"]})

    if merchant is None:
        return {"error": "Merchant not found"}

# NEW SECURITY CHECK
    if merchant.get("status") == "disabled":
        return {"error": "Merchant account is disabled"}

    if not verify_password(data["password"], merchant["password"]):
        return {"error": "Invalid password"}

    token = create_access_token({
        "merchant_id": str(merchant["_id"])
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "merchant_id": str(merchant["_id"])
    }


@router.get("/merchants")
def get_merchants():

    merchants = list(db.merchants.find())

    for m in merchants:
        m["_id"] = str(m["_id"])

    return merchants