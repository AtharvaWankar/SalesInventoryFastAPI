print("LOADING ITEM ROUTES")

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.schemas.item import (
    ItemCreate, ItemUpdate, ItemPartialUpdateQty, ItemResponse
)
from app.crud import item as crud_item
from app.utils.csv_utils import items_to_csv

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_alert(item):
    return ItemResponse(
        **item.__dict__,
        alert=item.qty < item.threshold
    )

@router.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = crud_item.create_item(db, item)
    return add_alert(db_item)

@router.get("/items/", response_model=List[ItemResponse])
def list_items(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    items = crud_item.get_items(db, skip=skip, limit=limit)
    return [add_alert(i) for i in items]

@router.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud_item.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return add_alert(db_item)

@router.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud_item.update_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return add_alert(db_item)

@router.patch("/items/{item_id}/quantity", response_model=ItemResponse)
def update_item_quantity(item_id: int, qty_update: ItemPartialUpdateQty, db: Session = Depends(get_db)):
    db_item = crud_item.update_item_qty(db, item_id, qty_update.qty)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return add_alert(db_item)

@router.delete("/items/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud_item.delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return add_alert(db_item)

@router.get("/items/search/", response_model=List[ItemResponse])
def search_items(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    items = crud_item.search_items_by_name(db, name)
    return [add_alert(i) for i in items]

@router.get("/items/alerts/", response_model=List[ItemResponse])
def get_alert_items(db: Session = Depends(get_db)):
    items = crud_item.get_items_below_threshold(db)
    return [add_alert(i) for i in items]

@router.post("/items/bulk/", response_model=List[ItemResponse])
def bulk_create_items(items: List[ItemCreate], db: Session = Depends(get_db)):
    db_items = crud_item.bulk_create_items(db, items)
    return [add_alert(i) for i in db_items]

@router.get("/items/download/")
def download_items_csv(db: Session = Depends(get_db)):
    items = crud_item.get_items(db, skip=0, limit=10000)
    csv_data = items_to_csv(items)
    return Response(content=csv_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=items.csv"})