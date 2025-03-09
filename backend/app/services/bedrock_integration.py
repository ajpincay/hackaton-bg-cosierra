import boto3
import json

# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")  # Update region if needed

INFERENCE_PROFILE_ARN = "arn:aws:bedrock:us-west-2:518847936203:inference-profile/us.amazon.nova-pro-v1:0"

def bedrock_model_adjustment(data: dict) -> float:
    """
    Calls AWS Bedrock AI Model (Nova-Pro) with the correct request format.
    """

    # Convert input data into the correct format
    system_list = [
        {"text": "You are an AI assistant that provides numerical score adjustments."}
    ]

    # Correctly formatted messages (without "system" inside messages)
    message_list = [
        {"role": "user", "content": [{"text": f"Adjust the score for: {json.dumps(data)}"}]}
    ]


    inf_params = {"maxTokens": 100, "temperature": 0.7, "topP": 0.9, "topK": 20}

    # Correct request format for Nova-Pro
    request_body = {
        "schemaVersion": "messages-v1",
        "messages": message_list,
        "system": system_list,  # System is separate
        "inferenceConfig": inf_params,
    }

    try:
        # Invoke model with the correct payload format
        response = bedrock.invoke_model(
            modelId=INFERENCE_PROFILE_ARN,  # Correct model ID
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body),
        )

        # Parse response
        response_body = json.loads(response["body"].read())
        print(response_body)
        # Extract score (assuming AI provides a numerical response)
        score_str = response_body.get("completion", "0").strip()
        score = float(score_str) if score_str.replace('.', '', 1).isdigit() else 0.0

        return score

    except Exception as e:
        print(f"Error calling AWS Bedrock: {e}")
        return 0.0
