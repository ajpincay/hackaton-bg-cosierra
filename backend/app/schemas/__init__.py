# app/schemas/__init__.py
from .pymes import (
    LoginRequest,
    LoginResponse,
    UserProfile,
    DashboardData,
    BankPortalData,
    CertificationData,
    CertificationsResponse,
    ConfidenceDetail,
    ConfidenceResponse,
    NetworkRecommendation,
    NetworkResponse,
)

from .external_data import (
    PersonaQueryParams,
    AutoQueryParams,
    EstablecimientoQueryParams,
    SalarioQueryParams,
    ScoreburoQueryParams,
    SuperciaQueryParams,
)

__all__ = [
    "LoginRequest",
    "LoginResponse",
    "UserProfile",
    "PersonaQueryParams",
    "AutoQueryParams",
    "EstablecimientoQueryParams",
    "SalarioQueryParams",
    "ScoreburoQueryParams",
    "SuperciaQueryParams",
    "DashboardData",
    "BankPortalData",
    "CertificationData",
    "CertificationsResponse",
    "ConfidenceDetail",
    "ConfidenceResponse",
    "NetworkRecommendation",
    "NetworkResponse",
]
