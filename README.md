# Code Assistant
A lightweight **AI Code Assistant** that can **generate** and **explain** code.
Built with **LangChain + LangGraph**, grounded on the **HumanEval** dataset, and driven by **GPT-4-mini (via OpenRouter)**. 
Designed to be modular, easy to run locally (Streamlit), and easy to extend.

---

# Table of contents

* [What it does](#what-it-does)
* [Features](#features)
* [Project structure](#project-structure)
* [Installation](#installation)
* [Configuration](#configuration)
* [How it works (architecture)](#how-it-works-architecture)
* [Files & responsibilities](#files--responsibilities)
* [Running locally](#running-locally)
---

# What it does

This project exposes a small assistant that supports two main intents from users:

1. **Generate code** — produce code snippets via Retrieval-Augmented Generation (RAG) using HumanEval examples as context.
2. **Explain code** — provide clear, structured explanations of provided snippets using the LLM.

It classifies user intent, routes the request to the correct node, then returns structured JSON + human-friendly output in the Streamlit UI.

---

# Features

* Intent classification (generate vs explain)
* RAG pipeline for generation using **HumanEval** + **ChromaDB** embeddings
* Direct LLM explanations for `explain` requests
* Streamlit UI for local testing and demo
* Modular Python code (one file per major responsibility)

---

# Project structure

```
code-assistant/
├── explain_code.py
├── generate_code.py
├── initialchain.py
├── loading.py
├── main.py
├── prepare_data.py
├── requirements.txt
├── README.md         <- (you are copying this)
└── .env              <- (local secrets, not tracked)
```

---

# Installation

1. **Clone**

```bash
git clone https://github.com/yourusername/code-assistant.git
cd code-assistant
```

2. **Create virtual env & install**

```bash
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate        # Windows PowerShell
pip install -r requirements.txt
```

3. **Add secrets**
   Create a `.env` in the project root (do **not** commit it):

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

---

# Configuration

* `requirements.txt` contains all dependencies (LangChain, LangGraph, chromadb, streamlit, openrouter client, etc.).
* `loading.py` expects to read the OpenRouter key from the environment (`os.environ` or `python-dotenv`).

---

# How it works (architecture)

```
User input
   │
   ▼
initialchain.py  <-- classifies intent (generate | explain)
   │ (intent)
   ▼
router.py         <-- routes to node
   ├── generate_code.py  (RAG + LLM -> generated code)
   └── explain_code.py   (LLM -> structured explanation)
   │
   ▼
main.py (Streamlit UI)
```
# Files & responsibilities (detail)

### `loading.py`

* Load `.env` and environment variables (OpenRouter API key).
* Initialize LLM client (OpenRouter wrapper pointing at GPT-4-mini).
* Load HumanEval dataset files.
  
### `prepare_data.py`

* Create embeddings for each example and write to ChromaDB.
* Provide a smoke test retrieval function to ensure embeddings and indexing are correct.

### `initialchain.py`

* Prompt the LLM with a short classifier instruction to determine whether the user wants `generate` or `explain`.
* Returns a consistent JSON schema:

```json
{
  "intent": "generate" | "explain"
}
```

### `generate_code.py`

* Accepts user prompt.
* Performs nearest-neighbor search in ChromaDB (top K).
* Constructs a RAG prompt: include retrieved HumanEval examples as context, then the user instruction.
* Calls LLM and returns code + metadata (source examples used, retrieval scores).

### `explain_code.py`

* Accepts a code snippet (or code block + question).
* Sends a prompt guiding the LLM to produce:

  * Short summary (1–2 lines)
  * Line-by-line explanation
  * Complexity and edge cases (optional)
* Returns structured JSON + human output.

### `main.py`

* Streamlit frontend:

  * Text input / code input area
  * Intent display (what the classifier decided)
  * Results area (code/explanation)
  * Buttons for "Run classification", "Generate", "Explain"
* Central app state, handles wiring and error UI.

---

# Running locally

```bash
# Make sure .env is set
streamlit run main.py
```

Open the URL shown by Streamlit (usually `http://localhost:8501`).
