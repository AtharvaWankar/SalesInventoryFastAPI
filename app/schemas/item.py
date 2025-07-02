from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
    item_name: str = Field(..., example="USB‑C Cables")
    qty: int = Field(..., ge=0, example=45)
    threshold: int = Field(..., ge=0, example=50)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemPartialUpdateQty(BaseModel):
    qty: int = Field(..., ge=0, example=10)

class ItemInDB(ItemBase):
    id: int

    class Config:
        orm_mode = True

class ItemResponse(ItemInDB):
    alert: bool = False