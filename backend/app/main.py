from fastapi import FastAPI, HTTPException
import os
import boto3
from pydantic import BaseModel

app = FastAPI()

TABLE_NAME = os.environ.get("TABLE_NAME", "ItemsTable")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


class Item(BaseModel):
    id: str
    data: str


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Lambda"}


@app.get("/items")
def list_items():
    resp = table.scan()
    return resp.get('Items', [])


@app.post("/items")
def create_item(item: Item):
    table.put_item(Item=item.dict())
    return {"status": "created", "item": item}
