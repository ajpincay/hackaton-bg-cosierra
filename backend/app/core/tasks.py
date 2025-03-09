# app/tasks.py
import random
from typing import Tuple
from app.services.bedrock_integration import bedrock_model_adjustment
from app.models.pymes import TierEnum

def fetch_and_calculate_category(ruc: str):
    """
    Simulate fetching data from external sources and computing a trust score.
    Returns a new trust_score (int) and a new tier (int).
    """
    financial_health = random.uniform(0, 100)
    business_reputation = random.uniform(0, 100)
    digital_presence = random.uniform(0, 100)
    legal_status = random.uniform(0, 100)
    web_seo_metrics = random.uniform(0, 100)

    # Weighted scoring
    score = (
        0.40 * financial_health +
        0.25 * business_reputation +
        0.20 * digital_presence +
        0.10 * legal_status +
        0.05 * web_seo_metrics
    )

    # AI-based adjustment
    adjustment = bedrock_model_adjustment({
        "financial_health": financial_health,
        "business_reputation": business_reputation,
        "digital_presence": digital_presence,
        "legal_status": legal_status,
        "web_seo_metrics": web_seo_metrics
    })

    final_score = (score + adjustment) / 2
    new_trust_score = int(final_score)

    if final_score >= 85:
        new_tier = 2  # Platinum
    elif final_score >= 70:
        new_tier = 1  # Gold
    else:
        new_tier = 0  # Silver

    return new_trust_score, new_tier



def calculate_trust_score(ruc, persona, salario_data, supercia_data_persona, auto_data, establecimiento_data, scoreburo_data) -> Tuple[int, str]:
    """
    Mock function that calculates a random trust_score and assigns a tier.
    Tiers: 'N/A', 'Plata', 'Oro', 'Platino'
    """
    base_score = 5
        # Bonus for being an accepted client
    if persona.get("esCliente") == 1:
        base_score += 10
    if salario_data and len(salario_data) > 0:
        base_score += 10
    if supercia_data_persona and len(supercia_data_persona) > 0:
        base_score += 10
    if auto_data and len(auto_data) > 0:
        base_score += 5
    if establecimiento_data and len(establecimiento_data) > 0:
        base_score += 5
    if scoreburo_data and len(scoreburo_data) > 0:
        base_score += 10

    score = min(base_score, 100)
    if score >= 85:
        tier = TierEnum.PLATINO
    elif score >= 70:
        tier = TierEnum.ORO
    elif score >= 1:
        tier = TierEnum.PLATA
    else:
        tier = TierEnum.NA
    return score, tier