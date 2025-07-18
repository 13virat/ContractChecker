from utils.ollama import call_ollama

def extract_clauses_by_llm(text):
    prompt = f"""
You are a legal AI assistant.

Your task is to extract key legal clauses from the following agreement text. These clauses may not have explicit headers, so infer from the language and label accordingly.

Identify and extract the following clauses (if present):
- Confidentiality
- Termination
- Governing Law
- Force Majeure
- Indemnity

Respond in the following format (JSON):
{{
  "Confidentiality": "full text of clause here",
  "Termination": "full text of clause here",
  ...
}}

If a clause is missing, omit the key entirely.

Contract Text:
{text}
"""
    response = call_ollama(prompt)
    return parse_llm_clause_response(response)


def parse_llm_clause_response(response_text):
    """
    Parse LLM response that is expected in JSON-like format.
    """
    import json
    import re

    try:
        # Clean up any preamble or stray text
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if not match:
            return {}
        cleaned = match.group(0)
        return json.loads(cleaned)
    except Exception as e:
        print("⚠️ Error parsing LLM clause extraction:", e)
        return {}
