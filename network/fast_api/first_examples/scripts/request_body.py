from typing import Dict, Union

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


@app.post("/items/{item_id}")
async def create_item(
    item_id: int, item: Item, q: Union[str, None] = None
) -> Dict[str, Union[str, int]]:
    result = {"item_id": item_id, **item.model_dump()}
    # If query parameter is given
    if q:
        result.update({"q": q})
    # If tax is specified, update
    if result["tax"]:
        result.update({"price_with_tax": result["price"] + result["tax"]})
    return result
