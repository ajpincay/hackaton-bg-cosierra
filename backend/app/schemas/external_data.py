from pydantic import BaseModel
from typing import Optional

# Persona Query Parameters
class PersonaQueryParams(BaseModel):
    cedula: Optional[str] = None
    ciudadania: Optional[str] = None
    estadoCivil: Optional[str] = None
    esCliente: Optional[int] = None
    tipoPersona: Optional[str] = None
    pageNumber: int = 1
    pageSize: int = 1000

# Auto Query Parameters
class AutoQueryParams(BaseModel):
    cedula: Optional[str] = None
    marca: Optional[str] = None
    clase: Optional[str] = None
    pageNumber: int = 1
    pageSize: int = 1000

# Establishment Query Parameters
class EstablecimientoQueryParams(BaseModel):
    cedula: Optional[str] = None
    estadoContribuyente: Optional[str] = None
    tipoContribuyente: Optional[str] = None
    provincia: Optional[str] = None
    ciudad: Optional[str] = None
    actividad: Optional[str] = None
    pageNumber: int = 1
    pageSize: int = 1000

# Salario Query Parameters
class SalarioQueryParams(BaseModel):
    cedula: Optional[str] = None
    rucEmpresa: Optional[str] = None
    sector: Optional[str] = None
    pageNumber: int = 1
    pageSize: int = 1000

# Scoreburo Query Parameters
class ScoreburoQueryParams(BaseModel):
    cedula: Optional[str] = None
    marcaTarjeta: Optional[str] = None
    pageNumber: int = 1
    pageSize: int = 1000

# Supercia Query Parameters
class SuperciaQueryParams(BaseModel):
    cedula: Optional[str] = None
    tamanio: Optional[str] = None
    pageNumber: int = 1
    pageSize: int = 1000
