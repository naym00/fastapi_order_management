from typing import Union
from fastapi import FastAPI, Depends, Response, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import schemas as SCHEMA
from app.database import engine, SessionLocal
from app import models
from help.response.generic import Generic as RHELP
from sqlalchemy import or_, func
from typing import Optional
import uvicorn

app = FastAPI()
resp = RHELP()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.post('/item', status_code=status.HTTP_201_CREATED)
async def add_item(item: SCHEMA.ItemCreate, db: Session = Depends(get_db)):
    new_item = models.Item(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# Search
# Searching by name
@app.get('/item')
def search_items(
    response: Response,
    name: Optional[str] = Query(None, min_length=1, description='Partial name to search (case-insensitive)'),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    method_response = {}
    query = db.query(models.Item)
    if name:
        query = query.filter(func.lower(models.Item.name).contains(func.lower(name)))
    db_items = query.offset(skip).limit(limit).all()

    resp.g_u_d_single(db_items, response, method_response)
    return method_response

# Search
# Searching by id
@app.get('/item/{id}', status_code=status.HTTP_200_OK)
async def one_item(id: int, response: Response, db: Session = Depends(get_db)):
    method_response = {}
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    resp.g_u_d_single(db_item, response, method_response)
    return method_response

@app.put('/item/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_item(id: int, response: Response, item: SCHEMA.ItemUpdate, db: Session = Depends(get_db)):
    method_response = {}
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    if resp.g_u_d_single(db_item, response, method_response):
        for key, value in item.model_dump().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return method_response

@app.patch('/item/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_item(id: int, response: Response, item: SCHEMA.ItemUpdate, db: Session = Depends(get_db)):
    method_response = {}
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    if resp.g_u_d_single(db_item, response, method_response):
        update_data = item.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return method_response

@app.delete('/items/{id}')
def delete_item(id: int, response: Response, db: Session = Depends(get_db)):
    method_response = {}
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    if resp.g_u_d_single(db_item, response, method_response):
        db.delete(db_item)
        db.commit()
        method_response.update({'message': 'Item deleted'})
    return method_response

# @app.get('/item/{id}', status_code=status.HTTP_200_OK)
# async def all_item(id: int, db: Session = Depends(get_db)):
#     item = db.query(models.Item).filter(models.Item.id == id).first()
#     if not item:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={"error": "Item not found"}
#         )
#     return item



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