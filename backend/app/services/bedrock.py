from typing import Dict
from app.core.utils import extract_json
import boto3
import json
from ratelimit import limits, sleep_and_retry

# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")  # Update region if needed

INFERENCE_PROFILE_ARN = "arn:aws:bedrock:us-west-2:518847936203:inference-profile/us.amazon.nova-pro-v1:0"

@sleep_and_retry
@limits(calls=1, period=1)
def generative_model(
    prompt: str, 
    system_instructions: list = None, 
    messages: list = None, 
    inference_params: dict = None
) -> str:
    """
    Calls an AWS Bedrock generative AI model with a customizable prompt, system instructions, and inference parameters.

    Args:
        prompt (str): The main input prompt for the model.
        system_instructions (list, optional): System messages guiding the AI's behavior.
        messages (list, optional): List of conversation messages in AWS Bedrock format.
        inference_params (dict, optional): Model inference parameters (e.g., maxTokens, temperature).

    Returns:
        str: Model's generated response.
    """

    # Assign default values if not provided
    system_instructions = system_instructions or [
        {"text": "You are an advanced AI assistant that helps with text generation."}
    ]
    
    messages = messages or [{"role": "user", "content": [{"text": prompt}]}]
    
    inference_params = inference_params or {
        "maxTokens": 100, 
        "temperature": 0.7, 
        "topP": 0.9, 
        "topK": 40
    }

    # Construct request payload
    request_body = {
        "schemaVersion": "messages-v1",
        "messages": messages,
        "system": system_instructions,
        "inferenceConfig": inference_params,
    }

    try:
        # Invoke AWS Bedrock model
        bedrock = boto3.client("bedrock-runtime")
        response = bedrock.invoke_model(
            modelId=INFERENCE_PROFILE_ARN,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body),
        )
        
        # Parse response body
        response_body = json.loads(response["body"].read())
        output = response_body.get("output", {})

        if isinstance(output, dict):
            output_text = output.get("message", {}).get("content", [])
            return output_text[0].get("text", "") if output_text and isinstance(output_text[0], dict) else ""

        return json.loads(output) if isinstance(output, str) else ""

    except Exception as e:
        print(f"Error during model invocation: {e}")
        return ""

    except Exception as e:
        print(f"Error calling AWS Bedrock: {e}")
        return {}

def generate_financial_summary(metrics: Dict, language: str = "spanish") -> Dict:
    """Use Bedrock Nova-1 to generate a financial summary."""
    prompt = f"""
    Given the following financial metrics:
   {
         json.dumps(metrics, indent=4)
   }

    Provide an analysis of the financial health and creditworthiness of this SME  in {language}.
    For the answer, respond with a structured JSON object in the format: {{"summary": "Your financial summary here", "recommendation": "Your recommendation here"}}
    """

    response_text = generative_model(
        prompt,
        system_instructions=[{"text": "You are a financial risk analyst That will always answer only with the given schema."}],
        inference_params={"maxTokens": 1024, "temperature": 0.7, "topP": 0.9, "topK": 40},
    )

    try:
        # Parse the extracted JSON
        response_json = extract_json(response_text)
        return response_json
    except (ValueError, json.JSONDecodeError, TypeError) as e:
        print(f"Invalid response received: {response_text}, Error: {e}")
        return {}

def bedrock_model_adjustment(data: dict) -> float:
    """
    Calls AWS Bedrock AI Model (Nova-Pro) for numerical score adjustments.
    Returns the adjusted score in a structured JSON format.
    """
    
    # Define system instructions
    system_instructions = [
        {"text": f"Adjust the score for the given data: {json.dumps(data)}. Return only a JSON object in the format {{\"evaluated_score\": value}} where value is a numerical score."}
    ]
    
    # Define inference parameters
    inference_params = {"maxTokens": 50, "temperature": 0.7, "topP": 0.9, "topK": 20}
    
    # Call the generative model
    response_text = generative_model(
        prompt="Adjust the score based on the given data. Answer only with the given schema.",
        system_instructions=system_instructions,
        inference_params=inference_params,
    )
    try:
        # Parse the extracted JSON
        response_json = extract_json(response_text)
        score = float(response_json.get("evaluated_score", 0.0))
        return score
    except (ValueError, json.JSONDecodeError, TypeError) as e:
        print(f"Invalid response received: {response_text}, Error: {e}")
        return 0.0

@sleep_and_retry
@limits(calls=1, period=1)  # Allow 1 call per second
def get_titan_embedding(text: str) -> list:
    """Generate an embedding using Amazon Titan Text Embeddings V2."""
    
    try:
        # Correct request format
        request_body = {"inputText": text}
        
        # Invoke the model
        response = bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body),
        )
        
        # Parse response
        response_body = json.loads(response["body"].read())

        # Extract embedding
        embedding = response_body.get("embedding", [])


        return embedding

    except Exception as e:
        print(f"Error generating Titan embedding: {e}")
        return []
