from pydantic import BaseModel
from .database import SessionLocal
#Step 3 : Pydantic Model

#1Base
class ItemBase(BaseModel):
    Title:str
    Description : str
    Price : float
    Type:str
    InStock:int

#2Request
class ItemCreate(ItemBase):
    pass

#3Response
class ItemResponse(ItemBase):
    id : int
    class Config:
        from_attributes= True