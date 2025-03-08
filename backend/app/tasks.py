# app/tasks.py
import random
from app.bedrock_integration import bedrock_model_adjustment

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
