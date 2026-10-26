from utils import ask_ollama

def generate_titles(source):
    return ask_ollama(
        "Create exactly 5 distinct, attractive, accurate blog titles based on the content below. "
        "Use a numbered list, avoid clickbait, and output titles only.\n\nCONTENT:\n" + source,
        temperature=0.8
    )
