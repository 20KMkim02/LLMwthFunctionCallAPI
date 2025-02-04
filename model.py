from .database import Base
from sqlalchemy import Column , Integer , String

# Step 2 : ORM Class
class ItemDB(Base):
    __tablename__='Item'
    id=Column(Integer,primary_key=True)
    Title=Column(String,index=True)
    Description=Column(String,index=True)
    Type=Column(String)
    Price=Column(Integer,index=True)
    InStock=Column(Integer)