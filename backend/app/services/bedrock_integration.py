from typing import Dict
import boto3
import json
from ratelimit import limits, sleep_and_retry

# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")  # Update region if needed

INFERENCE_PROFILE_ARN = "arn:aws:bedrock:us-west-2:518847936203:inference-profile/us.amazon.nova-pro-v1:0"

@sleep_and_retry
@limits(calls=1, period=1)
def generative_model(prompt: str, system_instructions: list = None, messages: list = None, inference_params: dict = None) -> str:
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

    # Default system instructions if none are provided
    if system_instructions is None:
        system_instructions = [{"text": "You are an advanced AI assistant that helps with text generation."}]

    # Default user messages if none are provided
    if messages is None:
        messages = [{"role": "user", "content": [{"text": prompt}]}]

    # Default inference parameters if not provided
    if inference_params is None:
        inference_params = {"maxTokens": 200, "temperature": 0.7, "topP": 0.9, "topK": 40}

    # Construct the request body
    request_body = {
        "schemaVersion": "messages-v1",
        "messages": messages,
        "system": system_instructions,
        "inferenceConfig": inference_params,
    }

    try:
        # Invoke the model
        response = bedrock.invoke_model(
            modelId=INFERENCE_PROFILE_ARN,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body),
        )

        # Parse the response
        response_body = json.loads(response["body"].read())

        # Extract the generated text response
        completion = response_body.get("completion", "").strip()

        print("\nGenerated Response:")
        print(completion)

        return completion

    except Exception as e:
        print(f"Error calling AWS Bedrock: {e}")
        return ""


def generate_financial_summary(metrics: Dict, language: str = "spanish") -> str:
    """Use Bedrock Nova-1 to generate a financial summary."""
    prompt = f"""
    Given the following financial metrics:
    - Revenue: {metrics['ventas']}
    - Credit Capacity: {metrics['cupo_creditos']}
    - Probability of Default: {metrics['prob_morosidad']}
    - Tax-to-Sales Ratio: {metrics['tax_to_sales']}
    - Financing Ratio: {metrics['financing_ratio']}
    - Debt-to-Income Ratio: {metrics['debt_to_income']}
    - Trustworthiness: {metrics['confianza']}

    Provide an analysis of the financial health and creditworthiness of this SME  in {language}.
    """

    response = generative_model(
        prompt,
        system_instructions=[{"text": "You are a financial risk analyst."}],
    )

    response_body = json.loads(response["body"].read())
    return response_body.get("completion", "").strip()


def bedrock_model_adjustment(data: dict) -> float:
    """
    Calls AWS Bedrock AI Model (Nova-Pro) for numerical score adjustments.
    """

    # Define system instructions
    system_instructions = [
        {"text": "You are an AI assistant that provides numerical score adjustments."}
    ]

    # Create message format
    messages = [
        {"role": "user", "content": [{"text": f"Adjust the score for: {json.dumps(data)}"}]}
    ]

    # Define inference parameters
    inference_params = {"maxTokens": 100, "temperature": 0.7, "topP": 0.9, "topK": 20}

    # Call the generic generative model function
    response_text = generative_model(
        prompt="Adjust the score based on the given data.",
        system_instructions=system_instructions,
        messages=messages,
        inference_params=inference_params,
    )

    try:
        # Convert response to float if possible
        score = float(response_text) if response_text.replace('.', '', 1).isdigit() else 0.0
        return score

    except ValueError:
        print(f"Invalid response received: {response_text}")
        return 0.0
    


@sleep_and_retry
@limits(calls=1, period=1)  # Allow 1 call per second
def get_titan_embedding(text: str) -> list:
    """Generate an embedding using Amazon Titan Text Embeddings V2."""
    
    try:
        # Correct request format
        request_body = {"inputText": text}  # Use 'inputText' instead of 'text'
        
        # Invoke the model
        response = bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",  # Correct model ID
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body),
        )
        
        # Parse response
        response_body = json.loads(response["body"].read())

        # Extract embedding
        embedding = response_body.get("embedding", [])
        input_token_count = response_body.get("inputTextTokenCount", 0)

        print("\nYour input:")
        print(text)
        print(f"Number of input tokens: {input_token_count}")
        print(f"Size of the generated embedding: {len(embedding)}")
        print("Embedding:", embedding)

        return embedding

    except Exception as e:
        print(f"Error generating Titan embedding: {e}")
        return []
