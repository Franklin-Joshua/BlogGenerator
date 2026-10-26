from utils import ask_ollama

def generate_meta_description(source):
    result = ask_ollama(
        "Write one compelling, accurate SEO meta description for the content below. "
        "It MUST be 160 characters or fewer. Return only the description, no quotation marks.\n\n"
        + source,
        temperature=0.4
    )
    result = result.strip().strip('"')
    if len(result) > 160:
        result = result[:157].rsplit(" ", 1)[0].rstrip(".,;: ") + "..."
    return result
