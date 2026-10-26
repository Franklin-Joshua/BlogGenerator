from utils import ask_ollama

VALID_INTENTS = {
    "BLOG_GENERATION", "SUMMARY", "KEYWORD_GENERATION",
    "META_DESCRIPTION", "TITLE_GENERATION", "UNKNOWN"
}

def detect_intent(user_request):
    prompt = f"""
Classify the user's request into exactly ONE intent label.
Allowed labels:
- BLOG_GENERATION: asks to write/create/generate a blog or article
- SUMMARY: asks to summarize or shorten existing content
- KEYWORD_GENERATION: asks for SEO keywords or keyphrases
- META_DESCRIPTION: asks for an SEO meta description
- TITLE_GENERATION: asks for blog titles or headlines
- UNKNOWN: none of the above or unclear

Return only the label, with no explanation.
User request: {user_request}
"""
    result = ask_ollama(prompt, temperature=0).upper().strip()
    for line in result.splitlines():
        label = line.strip().strip("`* .")
        if label in VALID_INTENTS:
            return label
    for label in VALID_INTENTS:
        if label in result:
            return label
    return "UNKNOWN"
