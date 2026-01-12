# CA.gov RAG Web Scraper Agent

This project implements a Retrieval-Augmented Generation (RAG) agent that scrapes all California government services and their provider agencies from [ca.gov](https://www.ca.gov/services/list/), then enables semantic search and Q&A over the results.

## Features

- Robust web scraping (requests, BeautifulSoup)
- Extracts all service names and their provider agencies from CA.gov
- Outputs a single JSON file: agency name, agency website, and a list of service names per agency
- Local semantic search (sentence-transformers, MiniLM, FAISS)
- (Optional) LLM integration for question answering (Ollama)
- Easily extensible to new sites and data types

## Project Structure

- `scraper/` - Web scraping logic (`webscraper.py`)
- `rag/` - RAG pipeline (vector store, semantic search, LLM interface)
- `data/` - Output data (see `agency_services.json`)
- `main.py` - Entry point for scraping and search

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) For LLM answers, install Ollama and pull a model:
   ```bash
   # Download and install Ollama from https://ollama.com/download
   ollama pull llama2
   ollama serve
   ```
3. Run the agent:
   ```bash
   python main.py
   ```

## Data Output Format

The main output is `data/agency_services.json`, structured as:

```
[
  {
    "agency_name": "Department of Health Care Services",
    "agency_url": "https://www.dhcs.ca.gov/",
    "services": [
      "Access Care",
      "Apply for Medi-Cal",
      ...
    ]
  },
  ...
]
```

## Example Usage

- Scrape all CA.gov services and agencies
- Ask: "Which agency handles food stamps?"

---

See `.github/copilot-instructions.md` for AI agent guidance.
