from typing import Dict
from app.core.utils import extract_json
import json
from ratelimit import limits, sleep_and_retry

# Mock data to replace AWS Bedrock responses
MOCK_SUMMARY_RESPONSE = {
    "summary": "The company has stable cash flow and moderate credit risk.",
    "recommendation": "Consider extending credit with a moderate limit."
}

MOCK_SCORE_ADJUSTMENT = {"evaluated_score": 75.0}

MOCK_EMBEDDING = [0.1, 0.2, 0.3, 0.4, 0.5]

@sleep_and_retry
@limits(calls=1, period=1)
def generative_model(
    prompt: str, 
    system_instructions: list = None, 
    messages: list = None, 
    inference_params: dict = None
) -> str:
    """
    Mocked generative AI model function that returns fake data instead of calling AWS Bedrock.
    """
    return json.dumps(MOCK_SUMMARY_RESPONSE)


def generate_financial_summary(metrics: Dict, language: str = "spanish") -> Dict:
    """Generate a financial summary using mock data."""
    return MOCK_SUMMARY_RESPONSE


def bedrock_model_adjustment(data: dict) -> float:
    """
    Mock function for numerical score adjustments, returns fake data.
    """
    return MOCK_SCORE_ADJUSTMENT["evaluated_score"]


@sleep_and_retry
@limits(calls=1, period=1)
def get_titan_embedding(text: str) -> list:
    """Mock function that returns a fake embedding instead of calling AWS Titan."""
    return MOCK_EMBEDDING
