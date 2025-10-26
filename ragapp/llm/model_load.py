"""
Language model loader and inference module for RAG application.

This module handles loading the LFM2-1.2B-RAG model and generating answers
based on retrieved context. The model is loaded once at startup to avoid
repeated initialization overhead.
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
import json
import sys


def load_model(model_name="LiquidAI/LFM2-1.2B-RAG"):
    """
    Load the LFM2 language model and tokenizer from Hugging Face Hub.

    This function initializes the tokenizer and causal language model directly
    from Hugging Face Hub. The model will be automatically downloaded and cached
    in your home directory (~/.cache/huggingface/). The model is configured to
    run on CPU with float32 precision for compatibility.

    Args:
        model_name (str): Hugging Face model identifier. Default is "LiquidAI/LFM2-1.2B-RAG".
            Can also be a local path if you've downloaded the model.

    Returns:
        tuple: A tuple containing:
            - tokenizer (AutoTokenizer): Tokenizer for encoding/decoding text
            - model (AutoModelForCausalLM): The loaded language model

    Example:
        >>> tokenizer, model = load_model("LiquidAI/LFM2-1.2B-RAG")

    Note:
        First run will download ~2.5GB model. Subsequent runs use cached version.
    """
    print(f"Loading model: {model_name}")
    print("Note: First time download may take several minutes...")

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Load model without device_map to avoid accelerate dependency
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=torch.float32,       # Use float32 for CPU compatibility
        low_cpu_mem_usage=True     # Optimize memory usage
    )

    # Explicitly move model to CPU
    model = model.to('cpu')
    model.eval()  # Set to evaluation mode

    print("✓ Model loaded successfully!")
    return tokenizer, model


# Global model load (for performance optimization)
# Loading the model once at module import time avoids repeated initialization
# overhead when handling multiple requests
tokenizer, model = load_model()


def generate_answer(context: str, query: str,  max_new_tokens: int = 200) -> str:
    """
    Generate an answer based on context and query using the preloaded model.
    """
    prompt = f"""You are a helpful assistant.
Context:
{context}

Question:
{query}

Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():  # disable gradient computation for faster inference
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Remove the prompt part to return only the generated answer
    if "Answer:" in answer:
        answer = answer.split("Answer:", 1)[-1].strip()

    return answer


# --- CLI Interface for Node.js ---
# if __name__ == "__main__":
#     data = json.loads(sys.stdin.read())
#     context = data.get("context", "")
#     query = data.get("query", "")
#     result = generate_answer(context, query)
#     print(json.dumps({"answer": result}))