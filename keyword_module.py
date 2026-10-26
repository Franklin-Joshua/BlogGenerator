from utils import ask_ollama

def generate_keywords(source):
    return ask_ollama(
        "Generate 8-12 relevant SEO keywords or short keyphrases for the content below. "
        "Include a mix of primary and long-tail keywords. Return a clean bullet list only; "
        "do not add explanations.\n\nCONTENT:\n" + source,
        temperature=0.3
    )
