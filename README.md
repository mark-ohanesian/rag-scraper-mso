
# Reliable RAG Web Scraper Agent

This project implements a Retrieval-Augmented Generation (RAG) agent capable of scraping any website and answering questions based on the scraped content. Example use case: extracting department names and URLs from https://www.ca.gov/topics/ and its subpages.

## Features

- Modular web scraping (requests, BeautifulSoup)
- Data storage for semantic search (FAISS)
- Local embeddings (sentence-transformers, MiniLM)
- Optional LLM integration for question answering (Ollama, e.g. Llama 2)
- Easily extensible to new sites and data types

## Project Structure

- `scraper/` - Web scraping logic
- `rag/` - RAG pipeline (vector store, LLM interface)
- `data/` - Storage for scraped and processed data
- `main.py` - Entry point for running the agent

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

## Example Usage

- Scrape all department names and URLs for a topic at https://www.ca.gov/topics/assistance/
- Ask: "Which department handles food stamps?"

---

See `.github/copilot-instructions.md` for AI agent guidance.
