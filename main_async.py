from fastapi import FastAPI, HTTPException, Depends
from models_async import Item, DBItem, get_session, AsyncSession, select


# Instantiate the app
app = FastAPI(
    title="Testing",
    description="Inventario de herramientas",
    version="0.1.0",
)


# Create new item
@app.post("/items")
async def add_item(item: Item, db: AsyncSession = Depends(get_session)):
    db_item = DBItem(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


# Delete item
@app.delete("/items/{item_id}")
async def delete_item(
    item_id: int, db: AsyncSession = Depends(get_session)
) -> dict[str, Item]:
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=404, detail=f"Item with id {item_id} does not exist."
        )
    db.delete(db_item)
    db.commit()
    return {"deleted": db_item.__dict__}


# Get items
@app.get("/items")
async def get_items(db: AsyncSession = Depends(get_session)):
    results = await db.execute(select(DBItem))
    items = results.scalars().all()
    return {"items": items}
