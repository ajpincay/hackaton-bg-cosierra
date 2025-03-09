from fastapi import APIRouter, Depends
from app.services.external_data_service import ExternalDataService
from app.schemas import (
    PersonaQueryParams, AutoQueryParams, EstablecimientoQueryParams,
    SalarioQueryParams, ScoreburoQueryParams, SuperciaQueryParams
)

router = APIRouter()

@router.get("/persona")
def get_persona(params: PersonaQueryParams = Depends()):
    return ExternalDataService.get_persona(params.dict())

@router.get("/auto")
def get_auto(params: AutoQueryParams = Depends()):
    return ExternalDataService.get_auto(params.dict())

@router.get("/establecimiento")
def get_establecimiento(params: EstablecimientoQueryParams = Depends()):
    return ExternalDataService.get_establecimiento(params.dict())

@router.get("/salario")
def get_salario(params: SalarioQueryParams = Depends()):
    return ExternalDataService.get_salario(params.dict())

@router.get("/scoreburo")
def get_scoreburo(params: ScoreburoQueryParams = Depends()):
    return ExternalDataService.get_scoreburo(params.dict())

@router.get("/supercia")
def get_supercia(params: SuperciaQueryParams = Depends()):
    return ExternalDataService.get_supercia(params.dict())

@router.post("/refresh")
def refresh_external_data(source: str = "all"):
    sources = ["persona", "auto", "establecimiento", "salario", "scoreburo", "supercia"]

    if source != "all" and source not in sources:
        return {"error": "Invalid source"}

    return {"message": "Data refreshed", "data": ExternalDataService.refresh_all()}
