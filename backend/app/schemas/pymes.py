# app/schemas/pymes.py
from pydantic import BaseModel

class LoginRequest(BaseModel):
    ruc: str
    password: str

class LoginResponse(BaseModel):
    ruc: str
    pyme_name: str
    trust_score: int
    tier: int
    token: str

class UserProfile(BaseModel):
    ruc: str
    pyme_name: str
    trust_score: int
    tier: int
