import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "outputs", "generated_blog.txt")

def ask_ollama(prompt, temperature=0.7):
    """Send a prompt to the locally running Ollama chat API."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "think": False,
                "options": {"temperature": temperature}
            },
            timeout=300,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "").strip()
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Cannot connect to Ollama. Start Ollama and confirm it is running at "
            f"{OLLAMA_URL}. Then run: ollama pull {MODEL}"
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("Ollama took too long to respond. Try a shorter request.") from exc
    except requests.exceptions.HTTPError as exc:
        detail = ""
        try:
            detail = response.text
        except Exception:
            pass
        raise RuntimeError(f"Ollama API error: {detail or exc}") from exc

def ollama_status():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        r.raise_for_status()
        models = [m.get("name", "") for m in r.json().get("models", [])]
        if any(m == MODEL or m.startswith(MODEL + ":") for m in models):
            return True, f"Ollama is running and {MODEL} is available."
        return False, f"Ollama is running, but {MODEL} is not installed. Run: ollama pull {MODEL}"
    except Exception:
        return False, "Ollama is not reachable. Start Ollama and check the local API."

def save_blog(content):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    return OUTPUT_PATH
