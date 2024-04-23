from typing import Union, Dict
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    # Required attributes
    name: str
    price: float
    # Optional attributes
    description: Union[str, None] = None
    tax: Union[float, None] = None

app = FastAPI(title="Request Body")

@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item
