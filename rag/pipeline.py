
import faiss
import os
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import requests

class RAGPipeline:
    def __init__(self, embedding_dim=768, embedding_model_name='all-MiniLM-L6-v2', ollama_url='http://localhost:11434'):  # 768 for MiniLM
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.texts = []
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.ollama_url = ollama_url

    def embed(self, texts: List[str]):
        # Use local sentence-transformers for embeddings
        try:
            vectors = self.embedding_model.encode(texts, show_progress_bar=False)
            # Ensure shape is (n_texts, embedding_dim)
            if len(vectors) == 0 or vectors.shape[1] != self.embedding_dim:
                print(f"Embedding error: shape mismatch {vectors.shape}")
                return [np.zeros(self.embedding_dim).tolist() for _ in texts]
            return vectors
        except Exception as e:
            print(f"Embedding error: {e}")
            return [np.zeros(self.embedding_dim).tolist() for _ in texts]

    def add_texts(self, texts: List[str]):
        vectors = self.embed(texts)
        self.index.add(np.array(vectors).astype('float32'))
        self.texts.extend(texts)

    def query(self, question: str, top_k=3) -> List[str]:
        q_vec = self.embed([question])[0]
        D, I = self.index.search(np.array([q_vec]).astype('float32'), top_k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]

    def answer(self, question: str, model='llama2') -> str:
        context = "\n".join(self.query(question))
        prompt = f"Use the provided context to answer.\nContext:\n{context}\n\nQuestion: {question}"
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": model, "prompt": prompt},
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data.get('response', '').strip()
        except Exception as e:
            print(f"LLM error: {e}")
            return "Sorry, I couldn't answer the question."
