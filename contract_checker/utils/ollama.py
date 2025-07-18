import requests

def call_ollama(prev_text, curr_text=None):
    if curr_text is None:
        prompt = prev_text  # Single input: it's a prompt
    else:
        # Two inputs: assume it's a contract comparison
        prompt = f"""Compare the following two versions of a contract and explain what has changed:

### Previous Version:
{prev_text}

### Current Version:
{curr_text}

Respond with a clear summary of all changes.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
           
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        print("🔥 Error from Ollama:", e)
        return "⚠️ Failed to get response from Ollama."
