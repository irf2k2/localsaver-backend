from fastapi import APIRouter, HTTPException
from database import db
from passlib.context import CryptContext
from auth import create_access_token

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