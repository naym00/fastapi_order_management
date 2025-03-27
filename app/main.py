from typing import Union
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import schemas as SCHEMA
from app.database import engine, SessionLocal
from app import models
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()


@app.post("/item")
async def add_item(item: SCHEMA.Item, db: Session = Depends(get_db)):
    new_item = models.Item(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item



# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}


# # @app.get("/items/{item_id}")
# # def read_item(item_id: int, q: Union[str, None] = None):
# #     return {"item_id": item_id, "q": q}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/item/{item_id}")
# async def update_item(item_id: int, item: SCHEMA.Item):
#     dict_obj = item.model_dump()
#     print('type: ', type(dict_obj), 'obj ', dict_obj)
#     return item

# @app.put("/bucket/{bucket_id}")
# async def update_item(bucket_id: int, bucket: SCHEMA.Bucket):
#     dict_obj = bucket.model_dump()
#     print('type: ', type(dict_obj), 'obj ', dict_obj)
#     return bucket

# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=8000)