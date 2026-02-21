# Complete Usage Guide - LangChain Hugging Face RAG

## Overview

This is a production-ready template for building **Retrieval-Augmented Generation (RAG)** systems using:
- **LangChain**: Framework for LLM applications
- **Hugging Face**: Open-source models (local inference)
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings
- **PyTorch**: ML backend

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER DOCUMENTS                            │
│                  (PDFs, TXT files in data/)                      │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼ step 1: python src/ingest.py
┌──────────────────────────────────────────────────────────────────┐
│                    INGESTION PIPELINE                            │
│  1. Load documents        (TextLoader, PyPDFLoader)              │
│  2. Split chunks          (1000 chars, 200 overlap)              │
│  3. Generate embeddings   (sentence-transformers/all-MiniLM)     │
│  4. Build FAISS index     (L2 distance)                          │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│                    PERSISTED FAISS INDEX                         │
│              indexes/faiss_index.pkl (~10-100MB)                 │
│  Contains: [embeddings, texts, metadata, dimension]             │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼ step 2: python src/run.py
┌──────────────────────────────────────────────────────────────────┐
│                      QUERY PROCESSING                            │
│                                                                  │
│  User Input: "What is RAG?"                                      │
│       │                                                          │
│       ▼                                                          │
│  ┌────────────────────────────────────┐                         │
│  │  Embed Query (sentence-transformers)│                        │
│  │  Query vector: 384-dimensional     │                         │
│  └────────────────┬───────────────────┘                         │
│                   │                                              │
│                   ▼                                              │
│  ┌────────────────────────────────────┐                         │
│  │  Retrieve Top-K Docs (FAISS)       │                         │
│  │  K=3, L2 distance search            │                        │
│  └────────────────┬───────────────────┘                         │
│                   │                                              │
│                   ▼                                              │
│  ┌────────────────────────────────────┐                         │
│  │  Build Prompt (context + query)    │                         │
│  │  "You are helpful. Context: ...    │                         │
│  │   Question: What is RAG?"          │                         │
│  └────────────────┬───────────────────┘                         │
│                   │                                              │
│                   ▼                                              │
│  ┌────────────────────────────────────┐                         │
│  │  Generate Answer (google/flan-t5)  │                         │
│  │  text2text-generation pipeline     │                         │
│  └────────────────┬───────────────────┘                         │
│                   │                                              │
│                   ▼                                              │
│  "RAG is Retrieval-Augmented Generation, ..."                    │
└──────────────────────────────────────────────────────────────────┘
```

## File Structure

```
LangChain-Hugging-FaceRAG/
│
├── src/                              # Main application code
│   ├── ingest.py                     # Document processing & index builder
│   │   ├── load_documents()          # Load TXT and PDF files
│   │   ├── chunk_documents()         # Split into semantic chunks
│   │   └── build_faiss_index()       # Create vector index
│   │
│   ├── agent.py                      # RAG Agent class
│   │   ├── SimpleRAGAgent.__init__()  # Load index and models
│   │   ├── retrieve()                # Find similar documents
│   │   ├── make_prompt()             # Construct LLM prompt
│   │   └── answer()                  # Generate answer
│   │
│   └── run.py                        # Interactive CLI
│       └── main()                    # REPL for asking questions
│
├── data/                             # Input documents
│   ├── sample_guide.txt              # Example document
│   └── (add your PDFs and TXT here)
│
├── indexes/                          # Vector database storage
│   └── faiss_index.pkl               # Serialized FAISS index
│
├── tests/                            # Test suite
│   └── test_ingest.py                # Integration tests
│
├── .devcontainer/                    # Docker dev environment
│   ├── devcontainer.json
│   └── Dockerfile
│
├── .github/                          # GitHub Actions CI/CD
│   └── workflows/ci.yml              # Build and test pipeline
│
├── requirements.txt                  # Python dependencies
├── README.md                         # Original project README
├── ANALYSIS_REPORT.md                # Technical analysis
├── DEPLOYMENT_REPORT.md              # Setup progress report
└── USAGE_GUIDE.md                    # This file (comprehensive guide)
```

## Step-by-Step Usage

### 1. Prerequisites

```bash
# Check Python version (3.10+ required)
python3 --version

# Check disk space (need ~5GB for models)
df -h

# Check RAM (2-4GB recommended)
free -h
```

### 2. Initial Setup (One-time)

```bash
cd /tmp/LangChain-Hugging-FaceRAG

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import langchain, torch, faiss; print('OK')"
```

### 3. Add Your Documents

Create text files in the `data/` directory:

```bash
# Example: Copy existing documents
cp ~/Documents/myfile.pdf data/
cp ~/Documents/article.txt data/

# Supported formats:
# - Plain text (.txt)
# - PDF (.pdf)
# - Add more loaders in src/ingest.py as needed
```

Sample document format (data/sample_guide.txt):
```
Title: What is Machine Learning?

Machine learning is a subset of AI that enables 
systems to learn and improve from experience without 
being explicitly programmed...

[Add your documents here, one per file or multiple in same file]
```

### 4. Build the Index

```bash
python src/ingest.py \
  --data-dir ./data \
  --index-path ./indexes/faiss_index.pkl
```

**What happens**:
1. Scans `./data/` for `.txt` and `.pdf` files
2. Downloads embedding model (~90MB, cached after first run)
3. Splits documents into 1000-char chunks (200-char overlap)
4. Generates 384-dimensional embeddings for each chunk
5. Creates FAISS index for fast similarity search
6. Saves everything to `indexes/faiss_index.pkl`

**Progress output**:
```
Loading documents...
Loaded 3 documents. Chunking...
Total chunks: 125
Loading embedding model...
Encoding...  [████████████████] 100%
Embeddings dimension: 384
Building FAISS index...
Index saved to ./indexes/faiss_index.pkl
```

**Typical time**: 1-5 minutes (depends on document count)

### 5. Run Interactive Agent

```bash
python src/run.py --index ./indexes/faiss_index.pkl
```

**What you see**:
```
Agent ready. Type your question (Ctrl-C to quit).
>> What is RAG?

Answer:
RAG stands for Retrieval-Augmented Generation. It's a technique
that combines document retrieval with text generation to provide
more accurate and contextually aware responses...

>> Explain the main components

Answer:
The main components are: (1) Document database, (2) Embeddings,
(3) Vector search (FAISS), (4) Language model...

>> exit
Exiting.
```

**Tips**:
- Type `exit` or `quit` to exit
- Press `Ctrl-C` to interrupt
- Questions can be multi-sentence
- Model generates single response (not streaming)

### 6. Run Tests (Optional)

```bash
# Install pytest if needed
pip install pytest

# Run tests
pytest tests/test_ingest.py -v

# Expected output:
# tests/test_ingest.py::test_ingest_creates_index PASSED
```

## How Each Component Works

### Embedding Model: sentence-transformers/all-MiniLM-L6-v2

- **Purpose**: Convert text → numerical vectors
- **Output dimension**: 384
- **Size**: ~35 MB
- **Speed**: ~300 documents/second on CPU
- **Alternative models**:
  - all-MiniLM-L12-v2 (smaller, faster)
  - all-mpnet-base-v2 (larger, better quality)
  - paraphrase-MiniLM-L6-v2 (good for paraphrasing)

**How to change**:
Edit `EMBED_MODEL` in both:
- src/ingest.py (line ~11)
- src/agent.py (line ~7)

### Generation Model: google/flan-t5-small

- **Purpose**: Answer questions based on context
- **Type**: Instruction-tuned text-to-text
- **Size**: ~60 MB
- **Speed**: ~2 seconds per answer on CPU
- **Alternative models**:
  - google/flan-t5-base (better quality, slower)
  - google/flan-t5-large (best quality, much slower)
  - lmsys/fastchat-t5-3b-v1.0 (efficient alternative)

**How to change**:
Edit `MODEL_NAME` in src/agent.py (line ~8)

### Vector Database: FAISS

- **Purpose**: Fast similarity search
- **Algorithm**: IndexFlatL2 (Euclidean distance)
- **Time complexity**: O(n) per query but highly optimized
- **Memory**: Proportional to embedding dimension and document count
- **Advantages over alternatives**:
  - Pure Python CPU implementation
  - No external dependencies
  - Serializable (save/load easily)

**Advanced options**:
- HNSW index for larger datasets (>100k vectors)
- Product Quantization for memory efficiency
- IVF (Inverted File) for indexing speedup

## Configuration Options

### Chunk Size & Overlap (src/ingest.py)

```python
def chunk_documents(docs, chunk_size=1000, chunk_overlap=200):
    '''
    chunk_size: characters per chunk (1000 recommended)
    chunk_overlap: overlap between chunks (200 is ~20%)
    
    For different use cases:
    - Dense text: 500 chars, 100 overlap
    - Structured data: 1500 chars, 300 overlap
    - Code: 2000 chars, 500 overlap
    '''
```

### Retrieval Parameters (src/agent.py)

```python
def __init__(self, index_path, k=3, device=-1):
    '''
    k: number of documents to retrieve (default: 3)
    device: -1 for CPU, 0 for GPU
    
    Adjust based on needs:
    - k=1: Faster, exact answer only
    - k=5: More context, slower
    - k=10: Maximum context (may exceed model limits)
    '''
```

### Generation Parameters (src/agent.py)

```python
def answer(self, query):
    out = self.generator(
        prompt,
        max_length=512,    # Maximum tokens in response
        do_sample=False    # Deterministic (no randomness)
    )
```

## Performance Tips

### 1. Speed Up Index Building
```python
# Use fewer chunks for testing
python src/ingest.py \
  --data-dir ./data \
  --index-path ./indexes/test_index.pkl

# Use GPU for embeddings
# TODO: Add GPU support in ingest.py
```

### 2. Faster Queries
```python
# Reduce retrieved documents
agent = SimpleRAGAgent(index_path, k=1)  # 1 instead of 3

# Use smaller model
MODEL_NAME = "t5-small"  # ~60MB instead of 100MB+

# Reduce max_length
self.generator(...max_length=256...)
```

### 3. Better Accuracy
```python
# Increase retrieved documents
agent = SimpleRAGAgent(index_path, k=5)

# Use larger model
MODEL_NAME = "t5-base"

# Use better embeddings
EMBED_MODEL = "all-mpnet-base-v2"
```

## Common Issues & Solutions

### Issue: "CUDA out of memory"
```python
# Solution: Use CPU
device=-1  # Default, uses CPU

# Or use smaller models
# google/flan-t5-small instead of base/large
```

### Issue: Slow embedding generation
```bash
# Expected speed: ~300 docs/sec
# If slower: CPU might be throttled

# Check:
- Close other applications
- Monitor CPU: top (Mac/Linux) or Task Manager (Windows)
- Consider GPU for batch processing
```

### Issue: "Module not found: langchain_text_splitters"
```bash
pip install langchain-text-splitters langchain-community
```

### Issue: Large memory usage
```python
# In src/ingest.py:
# Process documents in batches instead of all at once
embeddings = embedder.encode(
    texts,
    batch_size=32,  # Process 32 at a time
    show_progress_bar=True,
    convert_to_numpy=True
)
```

## Next Steps & Enhancements

### Immediate
- [ ] Complete first index build
- [ ] Ask questions and verify answers
- [ ] Try with your own documents

### Short Term
- [ ] Add GPU support
- [ ] Implement conversation history
- [ ] Add Gradio UI (`gradio` already installed)
- [ ] Performance metrics and benchmarks

### Medium Term
- [ ] Multi-document summarization
- [ ] Query rewriting and expansion
- [ ] Citation/source tracking
- [ ] Fact verification

### Long Term
- [ ] Fine-tune models on your data
- [ ] Implement semantic caching
- [ ] Build REST API
- [ ] Deploy to cloud (AWS, GCP, Azure)

## Extending the Code

### Add a New Document Loader

```python
# In src/ingest.py
def load_documents(data_dir):
    docs = []
    for fname in os.listdir(data_dir):
        path = os.path.join(data_dir, fname)
        if fname.endswith(".docx"):
            from langchain_community.document_loaders import Docx2txtLoader
            loader = Docx2txtLoader(path)
            docs.extend(loader.load())
    return docs
```

### Add Query Logging

```python
# In src/agent.py
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def answer(self, query: str) -> str:
    logger.info(f"Query: {query}")
    contexts = self.retrieve(query)
    logger.info(f"Retrieved {len(contexts)} documents")
    ...
```

### Add Web UI with Gradio

```python
# save as: src/ui.py
import gradio as gr
from agent import SimpleRAGAgent

def create_app(index_path):
    agent = SimpleRAGAgent(index_path)
    
    def chat(query):
        return agent.answer(query)
    
    interface = gr.Interface(
        fn=chat,
        inputs="text",
        outputs="text",
        title="RAG Assistant"
    )
    return interface

if __name__ == "__main__":
    interface = create_app("./indexes/faiss_index.pkl")
    interface.launch()
```

## Deployment

### Local Development
Use as-is with `python src/run.py`

### Docker Container
Use the provided `.devcontainer/Dockerfile`

### Cloud Deployment
See `.github/workflows/ci.yml` for CI/CD example

## Resources

- **LangChain Docs**: https://python.langchain.com/
- **Hugging Face Models**: https://huggingface.co/models
- **FAISS Documentation**: https://github.com/facebookresearch/faiss
- **Sentence Transformers**: https://www.sbert.net/

## Summary

This RAG system demonstrates:
- Real-world NLP application
- Local LLM inference
- Vector similarity search
- Document processing pipeline
- Production-ready code structure

**Key advantages**:
✅ Local processing (privacy)
✅ No API costs
✅ Fast iteration
✅ Customizable
✅ Educational

Happy exploring! 🚀
