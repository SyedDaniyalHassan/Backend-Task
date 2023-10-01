from fastapi import FastAPI
from . import models
from .database import engine
from .routes.sales import router as sales_router
from .routes.inventory import router as inventory_router

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(sales_router, tags=["Sales"], prefix="/sales")
app.include_router(inventory_router, tags=["Inventory"], prefix="/inventory")