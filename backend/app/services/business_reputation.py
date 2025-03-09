import json
import time
from typing import Dict
from app.core.utils import extract_json
from app.services.bedrock import generative_model, get_titan_embedding

class BusinessAnalysisService:
    @staticmethod
    def analyze_business(ruc: str) -> Dict[str, float]:
        """
        Uses a single LLM call to evaluate reputation, digital presence, and legal status in one request.
        """
        prompt = f"""
        Analyze the business with RUC {ruc} based on the following factors:
        - Reputation: Consider customer sentiment, complaints, and business credibility.
        - Digital Presence: Evaluate SEO metrics, website activity, and social media presence.
        - Legal Status: Assess tax compliance, legal disputes, and regulatory filings.
        
        Return a JSON object in the format:
        {{
            "reputation_score": value,
            "digital_presence_score": value,
            "legal_compliance_score": value
        }}
        """
        response_text = generative_model(prompt)
        response_json = extract_json(response_text)
        
        return {
            "reputation_score": float(response_json.get("reputation_score", 50.0)),
            "digital_presence_score": float(response_json.get("digital_presence_score", 40.0)),
            "legal_compliance_score": float(response_json.get("legal_compliance_score", 70.0)),
        }

    @staticmethod
    def get_business_embedding(ruc: str) -> list:
        """
        Generates an embedding for the business based on its RUC, which can be used for similarity comparisons.
        """
        return get_titan_embedding(f"Business RUC: {ruc}")

    @staticmethod
    def analyze_and_embed(ruc: str) -> Dict:
        """
        Performs business analysis and generates an embedding, ensuring one LLM call per second.
        """
        analysis_results = BusinessAnalysisService.analyze_business(ruc)
        time.sleep(1)  # Ensure we respect the 1 call per second limit
        embedding = BusinessAnalysisService.get_business_embedding(ruc)
        
        return {"analysis": analysis_results, "embedding": embedding}
