# RAG Chatbot - Complete Setup Guide

This guide will walk you through setting up and running the RAG (Retrieval-Augmented Generation) chatbot application.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Architecture Overview](#architecture-overview)
3. [Installation Steps](#installation-steps)
4. [Running the Application](#running-the-application)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **pip** (Python package manager)
- **npm** (Node package manager)

Verify installations:
```bash
python --version   # Should be 3.8 or higher
node --version     # Should be 16 or higher
npm --version
```

---

## Architecture Overview

The application has 3 main components:

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Chatbot System                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   Frontend   │─────▶│ FastAPI      │─────▶│  ChromaDB │ │
│  │   (React)    │      │ Python Server│      │  (Vector  │ │
│  │   Port 5173  │◀─────│  Port 8000   │◀─────│   Store)  │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│                              │                               │
│                              ▼                               │
│                        ┌──────────────┐                      │
│                        │  LFM2-1.2B   │                      │
│                        │  RAG Model   │                      │
│                        └──────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd /path/to/RAG-ragfull/ragapp
```

### Step 2: Set Up Python Backend

#### 2.1 Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

#### 2.2 Install Python Dependencies

```bash
# Install required packages
pip install fastapi uvicorn transformers torch sentence-transformers chromadb nltk
```

Or use the requirements file:
```bash
pip install -r pythonserver/requirements.txt
```

Additional required packages:
```bash
pip install sentence-transformers chromadb nltk
```

#### 2.3 Download the Language Model

**IMPORTANT:** The code currently uses a hardcoded path `D:/models/LFM2-1.2B-RAG`. You need to:

**Option A: Download the model to the default location**
```bash
# Create directory (adjust for your OS)
mkdir -p ~/models/LFM2-1.2B-RAG

# Run the model download script
cd /path/to/RAG-ragfull/ragapp
python llm/model_save.py
```

**Option B: Update the model path**
Edit `llm/model_load.py` and change line 16:
```python
def load_model(local_path="/path/to/models/LFM2-1.2B-RAG"):
```

### Step 3: Populate the Vector Database

Before running the server, you need to create the embeddings database:

```bash
cd /path/to/RAG-ragfull/ragapp

# Run the embedding pipeline
python -c "from embeder import embedder; embedder()"
```

This will:
- Load the TATQA dataset
- Create text chunks
- Generate embeddings
- Store them in ChromaDB (creates `./chroma_db` folder)

**Expected output:**
```
embedder started
Loading embedding model: all-MiniLM-L6-v2
Model loaded successfully.
Collection not found. Creating new one...
Inserted XXXX chunks into Chroma.
Embedding pipeline completed successfully!
```

### Step 4: Set Up Node.js Server (Optional)

The Node.js server is optional - the FastAPI server can work standalone.

```bash
cd /path/to/RAG-ragfull/ragapp/server

# Install dependencies
npm install
```

### Step 5: Set Up React Frontend

```bash
cd /path/to/RAG-ragfull/ragapp/client

# Install dependencies
npm install
```

---

## Running the Application

### Option 1: Full Stack (Recommended)

You need to run 2 services in separate terminals:

#### Terminal 1: Start FastAPI Backend

```bash
cd /path/to/RAG-ragfull/ragapp

# Activate virtual environment if not already active
source venv/bin/activate

# Start the FastAPI server
uvicorn pythonserver.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
Loading embedding model: all-MiniLM-L6-v2
Model loaded successfully.
```

**Test the backend:**
Open browser and go to:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/

#### Terminal 2: Start React Frontend

```bash
cd /path/to/RAG-ragfull/ragapp/client

# Start the development server
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

#### Access the Chatbot

Open your browser and navigate to:
```
http://localhost:5173
```

You should see the chat interface. Type a question and get AI-generated answers!

---

## Testing the System

### 1. Test Backend API Directly

Using curl:
```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the revenue?"}'
```

Or using the FastAPI interactive docs:
1. Go to http://localhost:8000/docs
2. Click on `/api/generate`
3. Click "Try it out"
4. Enter a query in the request body
5. Click "Execute"

### 2. Test Frontend

1. Open http://localhost:5173
2. Type a question in the chat input
3. Press Enter or click Send
4. You should receive an AI-generated answer

---

## Troubleshooting

### Issue 1: Model Not Found Error

**Error:**
```
FileNotFoundError: D:/models/LFM2-1.2B-RAG not found
```

**Solution:**
1. Download the model using `python llm/model_save.py`
2. Or update the path in `llm/model_load.py` to point to your model location

### Issue 2: ChromaDB Collection Not Found

**Error:**
```
Collection not found.
```

**Solution:**
Run the embedding pipeline:
```bash
python -c "from embeder import embedder; embedder()"
```

### Issue 3: CORS Errors in Browser

**Error:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
Ensure the FastAPI server is running with CORS enabled (it should be by default).
Check that the frontend is making requests to `http://localhost:8000/api/generate`

### Issue 4: Port Already in Use

**Error:**
```
Address already in use
```

**Solution:**
- For FastAPI (port 8000):
  ```bash
  uvicorn pythonserver.main:app --reload --port 8001
  ```
- For Frontend (port 5173):
  ```bash
  npm run dev -- --port 5174
  ```

### Issue 5: Module Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'sentence_transformers'
```

**Solution:**
Install missing dependencies:
```bash
pip install sentence-transformers chromadb nltk
```

### Issue 6: NLTK Data Missing

**Error:**
```
Resource punkt not found
```

**Solution:**
The app downloads it automatically, but you can also manually download:
```python
import nltk
nltk.download('punkt')
```

---

## Project Structure

```
RAG-ragfull/
├── ragapp/
│   ├── pythonserver/          # FastAPI backend
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── controllers/      # Business logic
│   │   └── routes/           # API endpoints
│   ├── data/                 # Data processing
│   ├── model/                # Embedding models
│   ├── llm/                  # Language models
│   ├── retriever/            # Retrieval logic
│   ├── vectorstore/          # ChromaDB management
│   ├── evaluation/           # Metrics
│   ├── client/               # React frontend
│   ├── server/               # Node.js server (optional)
│   ├── dataset/              # TATQA dataset
│   ├── chroma_db/            # Vector database (created after setup)
│   └── embeder.py            # Data ingestion script
```

---

## Quick Start Summary

```bash
# 1. Install Python dependencies
cd /path/to/RAG-ragfull/ragapp
pip install fastapi uvicorn transformers torch sentence-transformers chromadb nltk

# 2. Download and setup the model (update path in llm/model_save.py first!)
python llm/model_save.py

# 3. Create embeddings database
python -c "from embeder import embedder; embedder()"

# 4. Start backend (Terminal 1)
uvicorn pythonserver.main:app --reload --port 8000

# 5. Install frontend dependencies (Terminal 2)
cd client
npm install

# 6. Start frontend
npm run dev

# 7. Open browser to http://localhost:5173
```

---

## Environment Variables (Optional)

Create a `.env` file in the client directory:

```bash
# ragapp/client/.env
VITE_API_URL=http://localhost:8000
```

Create a `.env` file in the server directory (if using Node.js server):

```bash
# ragapp/server/.env
PORT=5000
```

---

## Production Deployment Tips

1. **Update CORS settings** in `pythonserver/main.py`:
   ```python
   allow_origins=["https://yourdomain.com"]  # Instead of ["*"]
   ```

2. **Use production ASGI server**:
   ```bash
   gunicorn pythonserver.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Build frontend**:
   ```bash
   cd client
   npm run build
   ```

4. **Configure model paths** via environment variables instead of hardcoding

---

## Need Help?

- Check all services are running (FastAPI backend, React frontend)
- Check browser console for errors (F12 → Console tab)
- Check terminal logs for error messages
- Ensure ChromaDB has been populated with embeddings
- Verify the model is downloaded and path is correct

---

## API Endpoints

### POST /api/generate
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
  "context": "Retrieved text chunks...",
  "answer": "Generated answer..."
}
```

---

Happy chatting with your RAG bot! 🤖
