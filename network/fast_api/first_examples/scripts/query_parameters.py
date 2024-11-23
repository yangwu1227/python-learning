from typing import Dict, Union, Optional

from fastapi import FastAPI

app = FastAPI(title="Multiple Path & Query Parameters")


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int,
    item_id: str,
    needy: str,
    q: Optional[str] = None,
    short: Optional[bool] = False,
) -> Dict[str, Union[int, str, object]]:
    """
    Path operation function to get a user's item.

    Parameters
    ----------
    user_id : int
        Path parameter
    item_id : str
        Path parameter
    needy : str
        This is a required query parameter
    q : Optional[str]
        Query parameter, by default None
    short : Optional[bool]
        Query parameter, by default False

    Returns
    -------
    Dict[str, Union[int, str, object]]
        A dictionary containing the user_id, item_id, and the needy query parameter
    """
    item = {"item_id": item_id, "owner_id": user_id, "needy": needy}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is a long description"})
    return item
