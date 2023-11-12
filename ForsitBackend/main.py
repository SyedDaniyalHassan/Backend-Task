import logging
from fastapi import FastAPI

from ForsitBackend.plogger import PLogger
from . import models
from .database import engine
from .routes.sales import router as sales_router
from .routes.inventory import router as inventory_router

logger = PLogger(name="my_fastapi_logger", level=logging.INFO).get_logger()
logger.info("Application Starting")
app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(sales_router, tags=["Sales"], prefix="/sales")
app.include_router(inventory_router, tags=["Inventory"], prefix="/inventory")