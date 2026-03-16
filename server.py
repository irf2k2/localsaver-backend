from fastapi import FastAPI

from routers import cities
from routers import categories
from routers import stores
from routers import deals
from routers import merchants
from routers import search
from routers import redemptions
from routers import admin

app = FastAPI(title="LocalSaver API")


app.include_router(cities.router)
app.include_router(categories.router)
app.include_router(stores.router)
app.include_router(deals.router)
app.include_router(merchants.router)
app.include_router(search.router)
app.include_router(redemptions.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "LocalSaver API Running"}