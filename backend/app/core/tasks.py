# app/tasks.py
import random
from typing import Tuple
from app.services.bedrock import bedrock_model_adjustment
from app.models.pymes import PymeTrust, TierEnum
from app.core.db import get_db
from app.services.api_hack_bg import AsyncExternalDataService
from app.core.sme_metrics import FinancialMetrics
from fastapi import Depends
from sqlalchemy.orm import Session

def determine_tier(score: int) -> TierEnum:
    """
    Determines the tier based on the given trust score.
    """
    if score >= 85:
        return TierEnum.PLATINO
    elif score >= 70:
        return TierEnum.ORO
    elif score >= 1:
        return TierEnum.PLATA
    return TierEnum.NA

def fetch_and_calculate_category(ruc: str, db: Session = Depends(get_db)) -> Tuple[int, TierEnum]:
    """
    Fetch data from external sources and computing a trust score.
    Returns a new trust_score (int) and a new tier (TierEnum).
    """
    factors = {
        "financial_health": random.uniform(0, 100),
        "business_reputation": random.uniform(0, 100),
        "digital_presence": random.uniform(0, 100),
        "legal_status": random.uniform(0, 100),
        "web_seo_metrics": random.uniform(0, 100),
    }

    # Obtain the actual trust score from the database
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()

    score = pyme.trust_score

    # AI-based adjustment
    adjustment = bedrock_model_adjustment(factors)
    final_score = (score + adjustment) / 2
    new_trust_score = int(final_score)
    new_tier = determine_tier(new_trust_score)

    return new_trust_score, new_tier

async def calculate_trust_score(
    ruc: str,
    persona: dict,
    salario_data: list,
    supercia_data_persona: list,
    auto_data: list,
    establecimiento_data: list,
    scoreburo_data: list
) -> Tuple[int, TierEnum]:
    """
    Function that calculates a trust_score and assigns a tier.
    """
    base_score = 5


    metrics = FinancialMetrics.calculate_metrics(
        {
            "persona": persona,
            "salario": salario_data,
            "supercia_persona": supercia_data_persona,
            "auto": auto_data,
            "establecimiento": establecimiento_data,
            "scoreburo": scoreburo_data
        }
    )
    
    base_score += metrics["Confidence Score"]

    score = min(base_score, 100)
    tier = determine_tier(score)
    
    return score, tier
