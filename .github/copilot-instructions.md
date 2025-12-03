# Copilot Instructions for AI Coding Agents

## Project Overview

This repository implements a Retrieval-Augmented Generation (RAG) agent that can scrape any website and answer questions based on the scraped content. Example: extracting department names and URLs from https://www.ca.gov/topics/ and subpages.

### Architecture

- `scraper/`: Web scraping logic (see `webscraper.py`).
- `rag/`: RAG pipeline (vector store, LLM interface; see `pipeline.py`).
- `data/`: Storage for scraped and processed data.
- `main.py`: Entry point for running the agent end-to-end.

### Key Workflows

- **Scraping**: Use `WebScraper` to extract topic and department links from a target site.
- **Data Storage**: Scraped data is saved as JSON in `data/`.
- **RAG Pipeline**: `RAGPipeline` embeds and stores text in FAISS, then uses OpenAI API for answering queries.
- **Run**: `python main.py` scrapes, stores, indexes, and answers a sample query.

### Conventions & Patterns

- All scraping logic is in `scraper/` and should be modular for new sites.
- RAG logic is in `rag/`, with clear separation between embedding, storage, and LLM calls.
- Use environment variable `OPENAI_API_KEY` for LLM access.
- Store all persistent data in `data/`.

### Dependencies

- Install with `pip install -r requirements.txt`.
- Key packages: `requests`, `beautifulsoup4`, `faiss-cpu`, `openai`, `tqdm`.

### Extending

- Add new scrapers in `scraper/` for other sites.
- Extend `RAGPipeline` for other vector stores or LLMs as needed.

---

_Last updated: 2025-12-03_
