# app/utils/csv_utils.py

import csv
from io import StringIO
from typing import List
from app.models.item import Item
from app.schemas.item import ItemCreate

def items_to_csv(items: List[Item]) -> str:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "item_name", "qty", "threshold"])
    for item in items:
        writer.writerow([item.id, item.item_name, item.qty, item.threshold])
    return output.getvalue()

def parse_items_csv(file_content: str) -> List[ItemCreate]:
    reader = csv.DictReader(StringIO(file_content))
    items = []
    for row in reader:
        items.append(ItemCreate(
            item_name=row["item_name"],
            qty=int(row["qty"]),
            threshold=int(row["threshold"])
        ))
    return items 