from fastapi import FastAPI
from typing import Dict

# FastAPI instance
app = FastAPI(title="First Endpoint")

@app.get("/")
async def first_endpoint() -> Dict[str, str]:
    """
    A coroutine to add a GET endpoint at the root path.

    Returns
    -------
    Dict[str, str]
        Response
    """
    return {"first": "endpoint"}
