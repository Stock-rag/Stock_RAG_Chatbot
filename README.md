# RAG Chatbot - Retrieval-Augmented Generation System

A complete RAG (Retrieval-Augmented Generation) chatbot application that answers questions using semantic search over the TATQA dataset combined with an LLM.

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- ~3GB disk space (for models)

### Installation & Running

#### Option 1: Using Shell Scripts (Easiest)

**Terminal 1 - Start Backend:**
```bash
cd /Users/brijeshmuralikrishnan/Downloads/RAG-ragfull
./run_backend.sh
```

**Terminal 2 - Start Frontend:**
```bash
cd /Users/brijeshmuralikrishnan/Downloads/RAG-ragfull
./run_frontend.sh
```

Then open your browser to: **http://localhost:5173**

#### Option 2: Manual Setup

See the complete guide: [SETUP_GUIDE.md](SETUP_GUIDE.md)

## What Does This Do?

This RAG chatbot:
1. **Retrieves** relevant text chunks from a vector database (ChromaDB)
2. **Augments** the query with retrieved context
3. **Generates** accurate answers using a language model (LFM2-1.2B-RAG)

### Example Query
**User:** "What is the company's revenue?"

**System:**
1. Converts query to embedding vector
2. Searches ChromaDB for similar text chunks
3. Retrieves top 2 most relevant paragraphs
4. Sends context + query to LLM
5. Returns generated answer

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│   React     │─────▶│   FastAPI    │─────▶│   ChromaDB   │
│  Frontend   │◀─────│   Backend    │◀─────│ Vector Store │
└─────────────┘      └──────────────┘      └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ LFM2-1.2B-RAG│
                     │    Model     │
                     └──────────────┘
```

## Project Structure

```
RAG-ragfull/
├── SETUP_GUIDE.md           # Detailed setup instructions
├── run_backend.sh           # Backend startup script
├── run_frontend.sh          # Frontend startup script
└── ragapp/
    ├── pythonserver/        # FastAPI backend
    ├── client/              # React frontend
    ├── data/                # Data processing modules
    ├── model/               # Embedding models
    ├── llm/                 # Language models
    ├── retriever/           # Retrieval logic
    ├── vectorstore/         # ChromaDB management
    ├── evaluation/          # Metrics & evaluation
    ├── dataset/             # TATQA dataset
    └── embeder.py           # Data ingestion pipeline
```

## Key Features

- **Semantic Search**: Uses SentenceTransformers for embedding-based retrieval
- **Vector Database**: ChromaDB for efficient similarity search
- **LLM Generation**: LFM2-1.2B-RAG model for answer generation
- **REST API**: FastAPI backend with automatic documentation
- **Modern UI**: React frontend with real-time chat interface
- **Evaluation Metrics**: Precision@k, Recall@k, and MRR

## Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **SentenceTransformers** - Text embedding (all-MiniLM-L6-v2)
- **ChromaDB** - Vector database for semantic search
- **Transformers** - LLM inference (LFM2-1.2B-RAG)
- **PyTorch** - Deep learning framework

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Axios** - HTTP client
- **TailwindCSS** - Styling

## API Endpoints

### `POST /api/generate`
Generate an answer using RAG

**Request:**
```json
{
  "query": "What is the revenue?"
}
```

**Response:**
```json
{
  "context": "Retrieved context chunks...",
  "answer": "The revenue is..."
}
```

### `GET /`
Health check endpoint

### `GET /docs`
Interactive API documentation (Swagger UI)

## Common Issues

### Model Not Found
```bash
# Download the model first
cd ragapp
python llm/model_save.py
```

### ChromaDB Not Populated
```bash
# Run the embedding pipeline
cd ragapp
python -c "from embeder import embedder; embedder()"
```

### Port Already in Use
```bash
# Use different ports
uvicorn pythonserver.main:app --port 8001
npm run dev -- --port 5174
```

## Data Flow

1. **Data Ingestion** (One-time setup)
   - Load TATQA dataset → Filter text questions → Create chunks → Generate embeddings → Store in ChromaDB

2. **Query Processing** (Runtime)
   - User query → Embed query → Search ChromaDB → Retrieve top-k chunks → Combine context → LLM generation → Return answer

## Performance

- **Retrieval**: ~100ms for semantic search
- **Generation**: ~2-5 seconds (CPU), ~500ms (GPU)
- **Total Response Time**: ~2-6 seconds

## Development

### Add New Endpoints
Edit `ragapp/pythonserver/routes/rag_routes.py`

### Modify Retrieval Logic
Edit `ragapp/retriever/chroma_retriever.py`

### Change Embedding Model
Edit `ragapp/model/embedding_model.py`

### Adjust LLM Parameters
Edit `ragapp/llm/model_load.py`

## Documentation

All code files include comprehensive docstrings and comments explaining:
- Purpose and functionality
- Parameters and return values
- Usage examples
- Important notes and warnings

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

Built with ❤️ using RAG technology
