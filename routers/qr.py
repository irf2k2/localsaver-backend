from fastapi import APIRouter, HTTPException
from utils.security import create_qr_token

router = APIRouter(
    prefix="/qr",
    tags=["QR"]
)


@router.get("/generate/{user_id}")
def generate_qr(user_id: str):
    """
    Generate a secure QR token for the user.
    This token will expire in 60 seconds.
    """

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    try:
        token = create_qr_token(user_id)

        return {
            "message": "QR generated successfully",
            "qr_token": token
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))