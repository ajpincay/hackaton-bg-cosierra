# schemas/pymes.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class LoginRequest(BaseModel):
    ruc: str
    password: str

class LoginResponse(BaseModel):
    ruc: str
    pyme_name: str
    trust_score: int
    tier: str
    token: Optional[str]

class UserProfile(BaseModel):
    ruc: str
    pyme_name: str
    trust_score: int
    tier: str
    financial_metrics: Optional[dict]

class DashboardData(BaseModel):
    trust_score: int
    tier: str
    recent_activity: list
    certifications_completed: int
    certifications_pending: int
    financial_summary: dict

class BankPortalData(BaseModel):
    welcome_message: str
    available_credit_lines: list
    application_status: str
    secure_messages: list

class CertificationData(BaseModel):
    name: str
    status: str  # e.g., "Completed", "Pending"

class CertificationCreate(BaseModel):
    name: str
    issuer: str
    issue_date: date
    expiration_date: date | None = None

class CertificationsResponse(BaseModel):
    certifications: list[CertificationData]

class ConfidenceDetail(BaseModel):
    factor_name: str
    value: float
    weight: float

class ConfidenceResponse(BaseModel):
    total_score: float
    tier: str
    breakdown: list[ConfidenceDetail]

class NetworkRecommendation(BaseModel):
    ruc: str
    pyme_name: str
    trust_score: int
    tier: str
    compatibility_score: float

class NetworkResponse(BaseModel):
    recommendations: list[NetworkRecommendation]

class PymeView(BaseModel):
    ruc: str
    pyme_name: str
    sector: str
    location: str
    peer_review: int
    connected: bool
    pending: bool

class PeerReviewCreate(BaseModel):
    peer_trust_score: int
