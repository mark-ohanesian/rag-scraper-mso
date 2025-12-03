
import faiss
import openai
import os
import numpy as np
from typing import List, Dict

class RAGPipeline:
    def __init__(self, embedding_dim=1536):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.texts = []

    def embed(self, texts: List[str]):
        # Use OpenAI embeddings (openai>=1.0.0)
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = api_key
        try:
            response = openai.embeddings.create(
                input=texts,
                model="text-embedding-ada-002"
            )
            # openai>=1.0.0 returns response.data as a list of dicts with 'embedding'
            vectors = [d['embedding'] for d in response.data]
            # Validate shape
            valid_vectors = [v for v in vectors if isinstance(v, list) and len(v) == self.embedding_dim]
            if len(valid_vectors) != len(texts):
                print(f"Warning: {len(texts) - len(valid_vectors)} embeddings missing or invalid.")
            # Pad missing vectors with zeros
            while len(valid_vectors) < len(texts):
                valid_vectors.append(np.zeros(self.embedding_dim).tolist())
            return valid_vectors
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

    def answer(self, question: str) -> str:
        context = "\n".join(self.query(question))
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = api_key
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Use the provided context to answer."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
                ]
            )
            return completion['choices'][0]['message']['content']
        except Exception as e:
            print(f"LLM error: {e}")
            return "Sorry, I couldn't answer the question."
