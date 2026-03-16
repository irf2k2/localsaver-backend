from fastapi import APIRouter
from database import db
from auth import hash_password, verify_password, create_access_token

router = APIRouter()


# ----------------------------
# User Registration
# ----------------------------
@router.post("/users/register")
def register_user(data: dict):

    data["password"] = hash_password(data["password"])
    data["status"] = "active"

    result = db.users.insert_one(data)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }


# ----------------------------
# User Login
# ----------------------------
@router.post("/users/login")
def login_user(data: dict):

    user = db.users.find_one({"email": data["email"]})

    if not user:
        return {"error": "User not found"}

    if user.get("status") == "disabled":
        return {"error": "User account disabled"}

    if not verify_password(data["password"], user["password"]):
        return {"error": "Invalid password"}

    token = create_access_token({
        "user_id": str(user["_id"])
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(user["_id"])
    }