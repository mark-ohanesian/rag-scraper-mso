
import faiss
import os
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import requests

class RAGPipeline:
    def __init__(self, embedding_dim=None, embedding_model_name='all-MiniLM-L6-v2', ollama_url='http://localhost:11434'):
        self.embedding_model = SentenceTransformer(embedding_model_name)
        # Auto-detect embedding dimension if not provided
        if embedding_dim is None:
            test_vec = self.embedding_model.encode(["test"])
            embedding_dim = test_vec.shape[1]
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.texts = []
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
        if not texts:
            print("Warning: No texts provided for embedding. Skipping add_texts.")
            return
        vectors = self.embed(texts)
        arr = np.array(vectors).astype('float32')
        if arr.size == 0:
            print("Warning: Embedding returned empty array. Skipping add_texts.")
            return
        # If only one text, arr may be 1D; reshape to (1, self.embedding_dim)
        if arr.ndim == 1:
            arr = arr.reshape(1, self.embedding_dim)
        self.index.add(arr)
        self.texts.extend(texts)

    def query(self, question: str, top_k=3) -> List[str]:
        if not self.texts:
            print("Warning: No texts indexed. Returning empty result from query.")
            return []
        q_vec = self.embed([question])[0]
        D, I = self.index.search(np.array([q_vec]).astype('float32'), top_k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]

    def answer(self, question: str, model='llama2') -> str:
        # Skip LLM call: just return the top context as the answer
        context = "\n".join(self.query(question))
        if not context:
            return "Sorry, I couldn't find an answer."
        return f"Top relevant context:\n{context}"
