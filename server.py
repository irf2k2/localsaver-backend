from fastapi import FastAPI

# ✅ Import all routers in same pattern
from routers.cities import router as cities_router
from routers.categories import router as categories_router
from routers.stores import router as stores_router
from routers.deals import router as deals_router
from routers.merchants import router as merchants_router
from routers.search import router as search_router
from routers.redemptions import router as redemptions_router
from routers.admin import router as admin_router
from routers.users import router as users_router
from routers.rewards import router as rewards_router
from routers.qr import router as qr_router
from routers.auth import router as auth_router
from routers.wallet import router as wallet_router
from routers.admin_wallet import router as admin_wallet_router


app = FastAPI(title="LocalSaver API")


# ✅ Include all routers
app.include_router(cities_router)
app.include_router(categories_router)
app.include_router(stores_router)
app.include_router(deals_router)
app.include_router(merchants_router)
app.include_router(search_router)
app.include_router(redemptions_router)
app.include_router(admin_router)
app.include_router(users_router)
app.include_router(rewards_router)
app.include_router(qr_router)
app.include_router(auth_router)
app.include_router(wallet_router)
app.include_router(admin_wallet_router)

@app.get("/")
def root():
    return {"message": "LocalSaver API Running"}