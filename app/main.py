from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.item import router as item_router
from app.database import Base, engine
from app.models.item import Item

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('app/static/index.html')

app.include_router(item_router, prefix="", tags=["items"])