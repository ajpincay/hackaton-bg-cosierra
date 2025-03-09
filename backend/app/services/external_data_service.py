import requests
from fastapi import HTTPException
from typing import Dict, Optional

BASE_URL = "https://api-hackathon-h0fxfrgwh3ekgge7.brazilsouth-01.azurewebsites.net/Hackathon"

class ExternalDataService:
    @staticmethod
    def fetch_data(endpoint: str, params: Dict, api_key: Optional[str] = None):
        headers = {"HCK-API-Key": api_key} if api_key else {}
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch data from {endpoint}")

        return response.json()

    @classmethod
    def get_persona(cls, params: Dict, api_key: Optional[str]):
        return cls.fetch_data("persona", params, api_key)

    @classmethod
    def get_auto(cls, params: Dict, api_key: Optional[str]):
        return cls.fetch_data("auto", params, api_key)

    @classmethod
    def get_establecimiento(cls, params: Dict, api_key: Optional[str]):
        return cls.fetch_data("establecimiento", params, api_key)

    @classmethod
    def get_salario(cls, params: Dict, api_key: Optional[str]):
        return cls.fetch_data("salario", params, api_key)

    @classmethod
    def get_scoreburo(cls, params: Dict, api_key: Optional[str]):
        return cls.fetch_data("scoreburo", params, api_key)

    @classmethod
    def get_supercia(cls, params: Dict, api_key: Optional[str]):
        return cls.fetch_data("supercia", params, api_key)

    @classmethod
    def refresh_all(cls, api_key: Optional[str]):
        sources = ["persona", "auto", "establecimiento", "salario", "scoreburo", "supercia"]
        return {source: cls.fetch_data(source, {"pageNumber": 1, "pageSize": 1000}, api_key) for source in sources}
