# Reliable RAG Web Scraper Agent

This project implements a Retrieval-Augmented Generation (RAG) agent capable of scraping any website and answering questions based on the scraped content. Example use case: extracting department names and URLs from https://www.ca.gov/topics/ and its subpages.

## Features

- Modular web scraping (requests, BeautifulSoup)
- Data storage for semantic search (FAISS)
- LLM integration for question answering (OpenAI API)
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
2. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your-key-here
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
