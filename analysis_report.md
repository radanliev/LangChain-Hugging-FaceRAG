# LangChain + Hugging Face RAG Repository - Analysis Report

## Project Overview
This is a **Retrieval-Augmented Generation (RAG)** starter project that demonstrates how to combine:
- **LangChain**: Framework for orchestrating language model applications
- **Hugging Face Models**: Local, open-source models for text generation and embeddings
- **FAISS**: Fast similarity search and clustering library for vector databases
- **Sentence Transformers**: For generating text embeddings

## Architecture

### Core Components

1. **Document Ingestion Pipeline** (`src/ingest.py`)
   - Loads text (.txt) and PDF documents from `data/` directory
   - Splits documents into chunks using `RecursiveCharacterTextSplitter` (1000 chars, 200 overlap)
   - Generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`
   - Builds and persists FAISS index with metadata

2. **RAG Agent** (`src/agent.py`)
   - `SimpleRAGAgent` class that:
     - Loads pre-built FAISS index
     - Retrieves top-k (default 3) similar documents for a query
     - Uses `google/flan-t5-small` for text generation
     - Constructs prompts with retrieved context
     - Generates answers using the local model

3. **Interactive Runner** (`src/run.py`)
   - Command-line interface for querying the RAG system
   - Takes index path as argument
   - Provides interactive loop for asking questions

## Workflow

```
1. Data Preparation
   └─> Place documents in data/ folder

2. Index Building
   └─> python src/ingest.py --data-dir ./data --index-path ./indexes/faiss_index.pkl
   └─> Creates embeddings and FAISS index

3. Query Processing
   └─> python src/run.py --index ./indexes/faiss_index.pkl
   └─> Interactive Q&A interface
```

## Models Used

| Component | Model | Purpose |
|-----------|-------|---------|
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 | Convert text to 384-dim vectors |
| Generation | google/flan-t5-small | CPU-friendly question answering |
| Vector DB | FAISS (CPU) | Fast similarity search |

## Key Features

✅ **Local Processing**: All models run locally, no API calls needed
✅ **Privacy**: Data stays on your machine
✅ **Cost Effective**: Uses CPU-friendly models
✅ **Modular Design**: Easy to swap models
✅ **CI/CD Ready**: Includes GitHub Actions workflow
✅ **DevContainer**: Includes Docker dev environment

## Dependencies

- **LangChain** >= 0.0.300: Orchestration framework
- **Transformers** >= 4.35.0: Hugging Face model integration
- **Sentence-Transformers** >= 2.2.2: Embedding models
- **FAISS-CPU** >= 1.7.3: Vector database
- **PyTorch**: ML framework (installed with transformers)
- **Python 3.10+**: Required for compatibility

## File Structure

```
LangChain-Hugging-FaceRAG/
├── src/
│   ├── ingest.py        # Document ingestion & index building
│   ├── agent.py         # RAG agent with retrieval + generation
│   └── run.py           # Interactive CLI
├── data/                # Input documents (TXT, PDF)
├── indexes/             # Persisted FAISS indexes
├── requirements.txt     # Python dependencies
├── .devcontainer/       # Docker dev environment
├── .github/workflows/   # GitHub Actions CI
└── tests/
    └── test_ingest.py   # Integration test
```

## Usage Instructions

### Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Build Index
```bash
python src/ingest.py --data-dir ./data --index-path ./indexes/faiss_index.pkl
```

### Run Interactive Agent
```bash
python src/run.py --index ./indexes/faiss_index.pkl
```

### Run Tests
```bash
pytest tests/test_ingest.py
```

## Customization Options

1. **Change Generation Model**: Edit `MODEL_NAME` in `src/agent.py`
   - For GPU: Use larger models like `google/flan-t5-large` or `lmsys/fastchat-t5-3b-v1.0`
   - For CPU: Keep `google/flan-t5-small`

2. **Change Embedding Model**: Edit `EMBED_MODEL` in both `src/ingest.py` and `src/agent.py`
   - Alternative: `all-MiniLM-L12-v2` (smaller), `all-mpnet-base-v2` (larger)

3. **Adjust Retrieval**: Change `k` parameter in agent initialization
   - Higher k = more retrieved documents = longer prompts

4. **Modify Chunking**: Edit `chunk_size` and `chunk_overlap` in `src/ingest.py`

## Performance Considerations

- **Index Building**: ~1-2 minutes for 10 documents on CPU
- **Query Time**: ~500ms-2s depending on model and hardware
- **Memory**: ~2-4GB for models + index
- **Disk**: Varies by document count (typically 100MB+ for models)

## Limitations

- **CPU Only**: Current config uses CPU embeddings and generation
- **Model Size**: Limited to smaller models for reasonable CPU performance
- **No Streaming**: Responses generated in full before display
- **Single Embedding**: Same embedding for all queries

## Production Recommendations

For production deployment:
1. Add guardrails and safety filters
2. Use GPU for faster inference
3. Implement caching for common queries
4. Add monitoring and logging
5. Consider using larger, more capable models
6. Implement rate limiting
7. Add input validation and sanitization

## GitHub Actions CI

The `.github/workflows/ci.yml` runs:
1. Checkout code
2. Setup Python 3.11
3. Install dependencies (cached)
4. Create sample data file
5. Build FAISS index from sample
6. Verify index was created (smoke test)

## Next Steps to Run

To get this project running:
1. ✅ Virtual environment created
2. ⏳ Install dependencies (pip install -r requirements.txt)
3. Add documents to `data/` folder
4. Run ingest.py to build index
5. Run run.py for interactive queries

(Note: Installation may take 5-10 minutes due to large ML dependencies like PyTorch)
