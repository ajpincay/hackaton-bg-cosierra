import json
import re

def extract_json(text):
    """
    Extracts a JSON object from a given text that contains `{}`.
    First attempts direct JSON parsing, then falls back to regex extraction if needed.
    Returns a single JSON object.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass  # If direct loading fails, attempt extraction
    
    # Regex pattern to extract JSON objects
    json_patterns = re.findall(r'\{.*?\}', text, re.DOTALL)
    print(json_patterns)
    for json_str in json_patterns:
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            continue
    
    return None