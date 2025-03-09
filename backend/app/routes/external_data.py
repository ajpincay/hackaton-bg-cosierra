import os
from fastapi import APIRouter, Depends
from typing import Optional
from app.services.external_data_service import ExternalDataService
from app.schemas import (
    PersonaQueryParams, AutoQueryParams, EstablecimientoQueryParams,
    SalarioQueryParams, ScoreburoQueryParams, SuperciaQueryParams
)

router = APIRouter(prefix="/external", tags=["ExternalData"])

# Load API key from environment
API_KEY = os.getenv("API_HCK_BG_KEY")

@router.get("/persona")
def get_persona(params: PersonaQueryParams = Depends()):
    return ExternalDataService.get_persona(params.dict(), API_KEY)

@router.get("/auto")
def get_auto(params: AutoQueryParams = Depends()):
    return ExternalDataService.get_auto(params.dict(), API_KEY)

@router.get("/establecimiento")
def get_establecimiento(params: EstablecimientoQueryParams = Depends()):
    return ExternalDataService.get_establecimiento(params.dict(), API_KEY)

@router.get("/salario")
def get_salario(params: SalarioQueryParams = Depends()):
    return ExternalDataService.get_salario(params.dict(), API_KEY)

@router.get("/scoreburo")
def get_scoreburo(params: ScoreburoQueryParams = Depends()):
    return ExternalDataService.get_scoreburo(params.dict(), API_KEY)

@router.get("/supercia")
def get_supercia(params: SuperciaQueryParams = Depends()):
    return ExternalDataService.get_supercia(params.dict(), API_KEY)

@router.post("/refresh")
def refresh_external_data(source: str = "all"):
    sources = ["persona", "auto", "establecimiento", "salario", "scoreburo", "supercia"]

    if source != "all" and source not in sources:
        return {"error": "Invalid source"}

    return {"message": "Data refreshed", "data": ExternalDataService.refresh_all(API_KEY)}
