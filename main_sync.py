from fastapi import FastAPI, HTTPException, Depends
from models_sync import Item, DBItem, Session, get_session


# # esto estaría en una base de datos
# items = {
#     0: Item(name='Hammer', price=9.99, quantity=20, id=0, category=Category.TOOLS),
#     1: Item(name='Pliers', price=5.99, quantity=20, id=1, category=Category.TOOLS),
#     2: Item(name='Nails', price=1.99, quantity=100, id=2, category=Category.CONSUMABLES),
# }


# Instantiate the app
app = FastAPI(
    title="Testing",
    description="Inventario de herramientas",
    version='0.1.0',
)

# Create new item
@app.post("/items")
def add_item(item: Item, db: Session = Depends(get_session)):
    db_item = DBItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item 

# Delete item
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_session)) -> dict[str, Item]:
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=404, detail=f"Item with id {item_id} does not exist."
        )
    db.delete(db_item)
    db.commit()
    return {"deleted": db_item.__dict__}

# Get items
@app.get('/items')
def get_items(db: Session = Depends(get_session)):
    items = db.query(DBItem).all()
    return {'items': items}


### Lo que quedó de antes con 'items'
# # Get the items
# @app.get("/")
# def index() -> dict[str, dict[int, Item]]:
#     """Shows every item in stock"""
#     return {"items": items}

# # Get item by id
# @app.get("/items/{item_id}")
# def queryt_item_by_id(item_id: int) -> Item:
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail=f"Item with id {item_id} does not exist")
#     return items[item_id]

# # Query by parameters
# Selection = dict[
#     str, str | float | int | Category | None
# ]

# @app.get("/items/")
# def query_item_by_parameters(
#     name: str | None = None,
#     price: float | None = None, 
#     quantity: int | None = None, 
#     category: Category | None = None, 
# ) -> dict[str, Selection | list[Item]]:
#     def check_item(item: Item) -> bool:
#         return all(
#             (
#                 name is None or item.name == name, 
#                 price is None or item.price == price,
#                 quantity is None or item.quantity == quantity,
#                 category is None or item.category is category
#             )
#         )
#     selection = [item for item in items.values() if check_item(item)]
#     return {
#         "query": {"name": name, "price": price, "quantity": quantity, "category":category},
#         "selection": selection, 
#     }


# # Add item
# @app.post("/")
# def add_item(item: Item) -> dict[str, Item]:

#     if item.id in items:
#         raise HTTPException(status_code=400, detail=f"Item with id {item.id} already exists.")

#     items[item.id] = item
#     return {"added": item}


# # Update item
# @app.put("/items/{item_id}")
# def update_item(
#     item_id: int,
#     name: str | None = None,
#     price: float | None = None,
#     quantity: int | None = None,
#     category: Category | None = None,
# ) -> dict[str, Item]:
    
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail=f"Item with id {item_id} does not exist.")
#     if all(info is None for info in (name, price, quantity, category)):
#         raise HTTPException(
#             status_code=400, detail="No parameters provided for update."
#         )
#     item = items[item_id]
#     if name is not None:
#         item.name = name
#     if price is not None:
#         item.price = price
#     if quantity is not None:
#         item.quantity = quantity

#     return {"updated": item}


# @app.delete("/items/{item_id}")
# def delete_item(item_id: int) -> dict[str, Item]:
#     if item_id not in items:
#         raise HTTPException(
#             status_code=404, detail=f"Item with id {item_id} does not exist."
#         )
#     item = items.pop(item_id)
#     return {"deleted": item}