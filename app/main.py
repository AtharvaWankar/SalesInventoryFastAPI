from fastapi import FastAPI

from app.api.item import router as item_router
from app.database import Base, engine
from app.models.item import Item

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(item_router, prefix="", tags=["items"])