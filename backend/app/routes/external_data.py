from fastapi import APIRouter, Depends
from app.integrations.external_data_service import AsyncExternalDataService
from app.schemas import (
    PersonaQueryParams, AutoQueryParams, EstablecimientoQueryParams,
    SalarioQueryParams, ScoreburoQueryParams, SuperciaQueryParams
)

router = APIRouter()

@router.get("/persona")
async def get_persona(params: PersonaQueryParams = Depends()):
    return await AsyncExternalDataService.get_persona(params.dict())

@router.get("/auto")
async def get_auto(params: AutoQueryParams = Depends()):
    return await AsyncExternalDataService.get_auto(params.dict())

@router.get("/establecimiento")
async def get_establecimiento(params: EstablecimientoQueryParams = Depends()):
    return await AsyncExternalDataService.get_establecimiento(params.dict())

@router.get("/salario")
async def get_salario(params: SalarioQueryParams = Depends()):
    return await AsyncExternalDataService.get_salario(params.dict())

@router.get("/scoreburo")
async def get_scoreburo(params: ScoreburoQueryParams = Depends()):
    return await AsyncExternalDataService.get_scoreburo(params.dict())

@router.get("/supercia")
async def get_supercia(params: SuperciaQueryParams = Depends()):
    return await AsyncExternalDataService.get_supercia(params.dict())

@router.post("/refresh")
async def refresh_external_data(source: str = "all"):
    sources = ["persona", "auto", "establecimiento", "salario", "scoreburo", "supercia"]

    if source != "all" and source not in sources:
        return {"error": "Invalid source"}

    return {"message": "Data refreshed", "data": await AsyncExternalDataService.refresh_all()}
