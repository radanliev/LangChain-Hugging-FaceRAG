# LangChain-Hugging-FaceRAG
 Small LangChain + local Hugging Face RAG starter, a VS Code devcontainer, and a GitHub Actions workflow that builds the FAISS index and runs a smoke test

README.md
# LangChain + Local Hugging Face RAG Starter

Purpose
-------
Prototype a retrieval-augmented generation (RAG) agent using:
- Local HF generation model: `google/flan-t5-small`
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Vector DB: FAISS
- Orchestration: LangChain (lightweight use)

Prerequisites
-------------
- Python 3.10+
- Git
- (Optional) GPU + CUDA for larger models

Quick local install
-------------------
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt


# LangChain + Local Hugging Face RAG Starter

Purpose
-------
Prototype a retrieval-augmented generation (RAG) agent using:
- Local HF generation model: `google/flan-t5-small`
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Vector DB: FAISS
- Orchestration: LangChain (lightweight use)

Prerequisites
-------------
- Python 3.10+
- Git
- (Optional) GPU + CUDA for larger models

Quick local install
-------------------
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
