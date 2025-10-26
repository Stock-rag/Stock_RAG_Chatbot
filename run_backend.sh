#!/bin/bash

# RAG Chatbot Backend Startup Script
# This script starts the FastAPI backend server

echo "🚀 Starting RAG Chatbot Backend..."
echo "=================================="
echo ""

# Navigate to the ragapp directory
cd "$(dirname "$0")/ragapp"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✓ Found virtual environment"
    source venv/bin/activate
else
    echo "⚠ No virtual environment found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created"

    echo ""
    echo "📦 Installing Python dependencies..."
    pip install fastapi uvicorn transformers torch sentence-transformers chromadb nltk
fi

echo ""
echo "🔍 Checking if ChromaDB is populated..."
if [ ! -d "chroma_db" ]; then
    echo "⚠ ChromaDB not found. Running embedder to create it..."
    echo "   This may take a few minutes..."
    python -c "from embeder import embedder; embedder()"
    echo "✓ ChromaDB created successfully"
fi

echo ""
echo "🌟 Starting FastAPI server on http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo "   Press Ctrl+C to stop"
echo ""

uvicorn pythonserver.main:app --reload --host 0.0.0.0 --port 8000
