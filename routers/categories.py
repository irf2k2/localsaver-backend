from fastapi import APIRouter
from database import db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/")
def get_categories():
    categories = list(db.categories.find())

    for c in categories:
        c["_id"] = str(c["_id"])

    return categories