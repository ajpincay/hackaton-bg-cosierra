import os
import asyncio
import httpx
from fastapi import HTTPException
from typing import Dict

# Base API URL
BASE_URL = "https://api-hackathon-h0fxfrgwh3ekgge7.brazilsouth-01.azurewebsites.net/Hackathon"

class AsyncExternalDataService:
    """Asynchronous data fetcher for the API."""

    API_KEY = os.getenv("API_HCK_BG_KEY")

    @staticmethod
    async def fetch_data(endpoint: str, params: Dict, client: httpx.AsyncClient):
        """Asynchronously fetch data from an API endpoint."""
        headers = {"HCK-API-Key": AsyncExternalDataService.API_KEY} if AsyncExternalDataService.API_KEY else {}

        params = {**params, "pageNumber": 1, "pageSize": 100000}

        try:
            response = await client.get(f"{BASE_URL}/{endpoint}", params=params, headers=headers, timeout=10.0)
            response.raise_for_status()
            return response.json() or {}  # Return an empty dict if no data
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching {endpoint}: {e}")

    @classmethod
    async def get_persona(cls, params: Dict):
        """Fetch persona data."""
        async with httpx.AsyncClient() as client:
            return await cls.fetch_data("persona", params, client)

    @classmethod
    async def get_auto(cls, params: Dict):
        """Fetch auto data."""
        async with httpx.AsyncClient() as client:
            return await cls.fetch_data("auto", params, client)

    @classmethod
    async def get_establecimiento(cls, params: Dict):
        """Fetch establecimiento data."""
        async with httpx.AsyncClient() as client:
            return await cls.fetch_data("establecimiento", params, client)

    @classmethod
    async def get_salario(cls, params: Dict):
        """Fetch salario data."""
        async with httpx.AsyncClient() as client:
            return await cls.fetch_data("salario", params, client)

    @classmethod
    async def get_scoreburo(cls, params: Dict):
        """Fetch scoreburo data."""
        async with httpx.AsyncClient() as client:
            return await cls.fetch_data("scoreburo", params, client)

    @classmethod
    async def get_supercia(cls, params: Dict):
        """Fetch supercia data."""
        async with httpx.AsyncClient() as client:
            return await cls.fetch_data("supercia", params, client)

    @classmethod
    async def refresh_all(cls):
        """Refresh all data sources asynchronously."""
        sources = ["persona", "auto", "establecimiento", "salario", "scoreburo", "supercia"]
        
        async with httpx.AsyncClient() as client:
            tasks = [cls.fetch_data(source, {"pageNumber": 1, "pageSize": 1000}, client) for source in sources]
            results = await asyncio.gather(*tasks)

        return dict(zip(sources, results))  # Return results as a dictionary

    @classmethod
    async def get_all_data(cls, cedula: str):
        """Fetch all financial data for an SME using its RUC (company tax ID)."""
        endpoints = ["scoreburo", "supercia", "salario", "establecimiento", "auto"]
        
        async with httpx.AsyncClient() as client:
            tasks = [cls.fetch_data(endpoint, {"cedula": cedula}, client) for endpoint in endpoints]
            results = await asyncio.gather(*tasks)
        return dict(zip(endpoints, results))