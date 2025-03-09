import os
import requests
from fastapi import HTTPException
from typing import Dict, Optional

BASE_URL = "https://api-hackathon-h0fxfrgwh3ekgge7.brazilsouth-01.azurewebsites.net/Hackathon"

class ExternalDataService:
    # Load API key from environment
    API_KEY = os.getenv("API_HCK_BG_KEY")

    @staticmethod
    def fetch_data(endpoint: str, params: Dict):
        headers = {"HCK-API-Key": ExternalDataService.API_KEY} if ExternalDataService.API_KEY else {}
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch data from {endpoint}")

        return response.json()

    @classmethod
    def get_persona(cls, params: Dict):
        return cls.fetch_data("persona", params)

    @classmethod
    def get_auto(cls, params: Dict):
        return cls.fetch_data("auto", params)

    @classmethod
    def get_establecimiento(cls, params: Dict):
        return cls.fetch_data("establecimiento", params)

    @classmethod
    def get_salario(cls, params: Dict):
        return cls.fetch_data("salario", params)

    @classmethod
    def get_scoreburo(cls, params: Dict):
        return cls.fetch_data("scoreburo", params)

    @classmethod
    def get_supercia(cls, params: Dict):
        return cls.fetch_data("supercia", params)

    @classmethod
    def refresh_all(cls):
        sources = ["persona", "auto", "establecimiento", "salario", "scoreburo", "supercia"]
        return {source: cls.fetch_data(source, {"pageNumber": 1, "pageSize": 1000}) for source in sources}
