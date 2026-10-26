# AI Blog Content Generator (Streamlit + Ollama)

A modular blog-writing app powered locally by `qwen3:4b`. It generates blogs, five titles,
SEO keywords, a ~100-word summary, a meta description (maximum 160 characters), and detects
user intent to route requests.

## Requirements
- Python 3.10+
- [Ollama](https://ollama.com/) installed
- Enough RAM/VRAM to run `qwen3:4b`

## Run on Windows (PowerShell)

Open PowerShell in the `BlogGenerator` folder:

```powershell
ollama pull qwen3:4b
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run main.py
```

If PowerShell blocks activation, you can skip activation and install/run with your Python executable:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run main.py
```

Ollama normally runs as a background app. If the API is not available, open another terminal
and run `ollama serve`. The app uses `http://localhost:11434` by default.

## Optional configuration

PowerShell:
```powershell
$env:OLLAMA_MODEL = "qwen3:4b"
$env:OLLAMA_URL = "http://localhost:11434"
streamlit run main.py
```

## Project structure

```text
BlogGenerator/
├── main.py
├── input_module.py
├── blog_module.py
├── title_module.py
├── summary_module.py
├── keyword_module.py
├── meta_module.py
├── intent_module.py
├── utils.py
├── requirements.txt
├── README.md
├── outputs/
│   └── generated_blog.txt
└── models/
```

Generated content is local. The blog save button writes to `outputs/generated_blog.txt`.
