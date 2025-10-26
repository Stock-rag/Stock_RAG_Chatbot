#!/bin/bash

# RAG Chatbot Frontend Startup Script
# This script starts the React frontend development server

echo "🎨 Starting RAG Chatbot Frontend..."
echo "==================================="
echo ""

# Navigate to the client directory
cd "$(dirname "$0")/ragapp/client"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
    echo "✓ Dependencies installed"
fi

echo ""
echo "🌟 Starting React development server"
echo "   Frontend URL: http://localhost:5173"
echo "   Press Ctrl+C to stop"
echo ""

npm run dev
