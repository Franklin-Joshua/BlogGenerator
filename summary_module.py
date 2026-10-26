from utils import ask_ollama

def generate_summary(source):
    return ask_ollama(
        "Summarize the following blog in approximately 100 words. Preserve its main points "
        "and do not add facts that are not in the text.\n\nBLOG:\n" + source,
        temperature=0.3
    )
