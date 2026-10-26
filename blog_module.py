from utils import ask_ollama

def generate_blog(topic, style="Professional", tone="Informative", word_count=500):
    prompt = f"""
Write a complete, original blog post on: {topic}

Requirements:
- Writing style: {style}
- Tone: {tone}
- Target length: approximately {word_count} words.
- Include a clear title, engaging introduction, informative headings, useful examples where relevant,
  and a concise conclusion.
- Keep claims factual; do not invent statistics, citations, or sources.
- Output the blog only, with clean Markdown formatting.
"""
    return ask_ollama(prompt)
