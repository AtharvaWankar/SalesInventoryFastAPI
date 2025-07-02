# app/crud/item.py

from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from typing import List, Optional

def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemUpdate) -> Optional[Item]:
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    for field, value in item.dict().items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item_qty(db: Session, item_id: int, qty: int) -> Optional[Item]:
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    db_item.qty = qty
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> Optional[Item]:
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

def get_items_below_threshold(db: Session) -> List[Item]:
    return db.query(Item).filter(Item.qty < Item.threshold).all()

def search_items_by_name(db: Session, name: str) -> List[Item]:
    return db.query(Item).filter(Item.item_name.ilike(f"%{name}%")).all()

def bulk_create_items(db: Session, items: List[ItemCreate]) -> List[Item]:
    db_items = [Item(**item.dict()) for item in items]
    db.add_all(db_items)
    db.commit()
    for db_item in db_items:
        db.refresh(db_item)
    return db_items

def get_items_count(db: Session) -> int:
    return db.query(Item).count() 