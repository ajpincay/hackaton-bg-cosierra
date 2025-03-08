# app/models.py
from pydantic import BaseModel, HttpUrl
from typing import Optional

class UserProfile(BaseModel):
    user_id: str
    company_name: str
    tier: Optional[str] = None  # 'Silver', 'Gold', or 'Platinum'
    badge_url: Optional[HttpUrl] = None
    opted_in: bool = False

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    user_id: str
    token: str

class OptInRequest(BaseModel):
    user_id: str
    opt_in: bool

class CategoryRecalculationResponse(BaseModel):
    message: str