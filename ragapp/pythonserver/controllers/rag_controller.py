"""
RAG controller for handling answer generation requests.

This controller orchestrates the RAG pipeline: retrieving relevant context
from the vector database and generating answers using the language model.
"""

from llm.model_load import generate_answer
from retriever.chroma_retriever import chroma_retriever


def handle_generate_answer(query: str):
    """
    Handle RAG answer generation request.

    This function implements the complete RAG pipeline:
    1. Retrieve relevant text chunks from ChromaDB using semantic search
    2. Combine retrieved chunks into a single context string
    3. Generate an answer using the language model with the context

    Args:
        query (str): The user's question

    Returns:
        dict: Response containing:
            - context (str): Combined text chunks used for generation
            - answer (str): Generated answer from the language model

    Example:
        >>> result = handle_generate_answer("What is the revenue?")
        >>> print(result)
        {
            "context": "Q1 revenue was $1.2M...\nRevenue increased by 15%...",
            "answer": "The revenue for Q1 was $1.2 million..."
        }

    Process Flow:
        User Query -> Embedding -> ChromaDB Search -> Top 2 Chunks ->
        Combine Context -> LLM Generation -> Answer
    """
    # Step 1: Retrieve top 2 relevant chunks from vector database
    context = chroma_retriever(query)

    # Step 2: Combine chunks into a single context string
    combined_context = "\n".join(context)

    # Step 3: Generate answer using LLM with retrieved context
    answer = generate_answer(combined_context, query)

    # Return both context and answer for transparency
    return {"context": combined_context, "answer": answer}