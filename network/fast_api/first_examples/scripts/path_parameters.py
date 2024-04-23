from enum import Enum 
from typing import Dict
from fastapi import FastAPI

class CountryName(str, Enum):
    usa = "usa"
    japan = "japan"
    china = "china"
    
app = FastAPI(title="Country")

@app.get("/country/{country_name}")
async def get_country(country_name: CountryName) -> Dict[str, str]:
    """
    Path operation function to get a country's name.

    Parameters
    ----------
    country_name : CountryName
        Path parameter

    Returns
    -------
    Dict[str, str]
        Response
    """
    match country_name:
        case CountryName.usa:
            return {"country_name": country_name, "message": "Chicken Nuggets"}
        case CountryName.japan:
            return {"country_name": country_name, "message": "Samurai"}
        case CountryName.china:
            return {"country_name": country_name, "message": "Pandas"}
