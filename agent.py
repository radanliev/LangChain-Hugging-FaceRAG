# src/agent.py
import pickle
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from typing import List

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_NAME = "google/flan-t5-small"   # CPU-friendly generation model; swap for GPU models as needed

class SimpleRAGAgent:
    def __init__(self, index_path: str, k: int = 3, device: int = -1):
        with open(index_path, "rb") as f:
            state = pickle.load(f)
        self.index = state["index"]
        self.texts = state["texts"]
        self.metadata = state["metadata"]
        self.dim = state["dim"]
        self.k = k

        # embedding model
        self.embedder = SentenceTransformer(EMBED_MODEL)

        # generation pipeline: text2text-generation for Flan-T5
        # device=-1 uses CPU; for GPU set device=0
        self.generator = pipeline("text2text-generation", model=MODEL_NAME, device=device, truncation=True)

    def retrieve(self, query: str) -> List[str]:
        qvec = self.embedder.encode([query], convert_to_numpy=True)
        D, I = self.index.search(qvec, self.k)
        results = []
        for idx in I[0]:
            if idx < len(self.texts):
                results.append(self.texts[idx])
        return results

    def make_prompt(self, query: str, contexts: List[str]) -> str:
        context_text = "\n\n---\n\n".join(contexts)
        prompt = (
            "You are a helpful assistant. Use the following extracted context to answer the question. "
            "If the answer is not contained within the context, say you don't know.\n\n"
            f"Context:\n{context_text}\n\nQuestion: {query}\n\nAnswer:"
        )
        return prompt

    def answer(self, query: str) -> str:
        contexts = self.retrieve(query)
        prompt = self.make_prompt(query, contexts)
        # generator returns list of dicts
        out = self.generator(prompt, max_length=512, do_sample=False)
        return out[0]["generated_text"]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", required=True)
    args = parser.parse_args()
    agent = SimpleRAGAgent(args.index)
    while True:
        q = input("Question (or 'exit')> ").strip()
        if q.lower() in ("exit", "quit"):
            break
        print("\n--- Retrieved + Answer ---")
        print(agent.answer(q))
        print("---------------------------\n")
