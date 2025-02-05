from typing import Union,List,Optional
from fastapi import FastAPI ,Depends , HTTPException ,Query
from sqlalchemy.orm import Session 

from .schema import ItemCreate, ItemResponse,ItemBase
from .database import get_db, engine, Base
from .model import ItemDB


#Sync Schema -> สร้างฐานข้อมูล เทียบclass ORM กับ Database ถ้าตัวไหนหายไปจะได้สร้างรองรับไว้ก่อน
Base.metadata.create_all(bind=engine)

app =FastAPI()

#---------------------------------------------------------------------------

@app.post('/items',response_model=ItemResponse)
def create_item(item:ItemBase,db:Session= Depends(get_db)):
    # db_item=Item(title=item.title,description=item.description,price=item.price) อันนี้เป็นการadd ราย field
    #อันล่างจะเป็นการ add ทั้งหมด
    db_item= ItemDB(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    print(db_item)
    return db_item

# @app.get("/items/", response_model=List[ItemResponse])
# async def read_items(db: Session = Depends(get_db)):
#     return db.query(ItemDB).all()

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=List[ItemResponse])
async def read_items(
    db: Session = Depends(get_db), 
    query: Optional[str] = Query(None, min_length=1, description="Search query")
):
    items_query = db.query(ItemDB)
    
    if query:
        items_query = items_query.filter(ItemDB.Title.contains(query))
    
    items = items_query.all()
    return items

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}