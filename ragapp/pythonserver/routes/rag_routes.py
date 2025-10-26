"""
FastAPI routes for RAG endpoints.

This module defines the API routes for the RAG system, including request/response
models and endpoint handlers for answer generation.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from pythonserver.controllers.rag_controller import handle_generate_answer

# Initialize API router
router = APIRouter()


class QueryRequest(BaseModel):
    """
    Request model for answer generation endpoint.

    Attributes:
        query (str): The user's question to be answered using RAG
    """
    query: str


@router.post("/generate")
async def generate_endpoint(req: QueryRequest):
    """
    POST endpoint for generating RAG-based answers.

    This endpoint receives a user query, retrieves relevant context from the
    vector database, and generates an answer using the language model.

    Args:
        req (QueryRequest): Request body containing the user's query

    Returns:
        dict: Response containing:
            - context (str): Retrieved text chunks used for generation
            - answer (str): Generated answer from the LLM

    Example Request:
        POST /api/generate
        {
            "query": "What is the company's revenue?"
        }

    Example Response:
        {
            "context": "Revenue for Q1 was $1.2M...",
            "answer": "The company's revenue for Q1 was $1.2 million..."
        }

    Status Codes:
        - 200: Success - answer generated
        - 422: Validation error - invalid request format
        - 500: Internal server error - model or database issue
    """
    return handle_generate_answer(req.query)