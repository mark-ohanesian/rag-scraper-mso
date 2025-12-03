from scraper.webscraper import WebScraper
from rag.pipeline import RAGPipeline
import os
import json

def main():
    # Scrape departments for all topics
    scraper = WebScraper('https://www.ca.gov/topics/')
    topics = scraper.get_topic_links()
    all_depts = []
    for topic in topics:
        depts = scraper.get_departments(topic)
        all_depts.extend(depts)
    # Save scraped data
    os.makedirs('data', exist_ok=True)
    with open('data/departments.json', 'w', encoding='utf-8') as f:
        json.dump(all_depts, f, ensure_ascii=False, indent=2)
    # Prepare RAG pipeline
    rag = RAGPipeline()
    texts = [f"{d['name']}: {d['url']}" for d in all_depts]
    rag.add_texts(texts)
    # Example query
    question = "Which department handles food stamps?"
    answer = rag.answer(question)
    print(f"Q: {question}\nA: {answer}")

if __name__ == "__main__":
    main()
