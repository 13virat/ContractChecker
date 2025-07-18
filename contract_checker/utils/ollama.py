import requests

def call_ollama(prev_text, curr_text):
    prompt = f"""Compare the following two versions of a contract and explain what has changed:

### Previous Version:
{prev_text}

### Current Version:
{curr_text}

Respond with a clear summary of all changes.
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]
