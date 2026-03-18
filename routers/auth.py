from fastapi import APIRouter, HTTPException
from database import db
from jose import jwt
from utils.security import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/merchant/login")
def merchant_login(data: dict):

    email = data.get("email")
    password = data.get("password")

    merchant = db.merchants.find_one({"email": email})

    if not merchant or merchant.get("password") != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "merchant_id": str(merchant["_id"])
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer"
    }