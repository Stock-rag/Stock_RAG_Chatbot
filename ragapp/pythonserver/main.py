"""
FastAPI backend server for RAG application.

This module initializes and configures the FastAPI application that serves
the RAG (Retrieval-Augmented Generation) API endpoints. It handles CORS
configuration and routes registration.

Usage:
    Run with: uvicorn pythonserver.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pythonserver.routes.rag_routes import router as rag_router
import sys
import os

# Add parent directory to Python path to enable imports from ragapp modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Initialize FastAPI application
app = FastAPI(title="RAG API")

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the frontend (running on a different port) to make requests to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins (change in production for security)
    allow_credentials=True,     # Allow cookies and authentication headers
    allow_methods=["*"],        # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],        # Allow all headers
)

# Register RAG routes with /api prefix
# All RAG endpoints will be accessible at /api/...
app.include_router(rag_router, prefix="/api", tags=["RAG"])


@app.get("/")
def root():
    """
    Root endpoint for health check.

    Returns:
        dict: Simple message confirming the API is running

    Example:
        >>> GET /
        {"message": "RAG API running!"}
    """
    return {"message": "RAG API running!"}