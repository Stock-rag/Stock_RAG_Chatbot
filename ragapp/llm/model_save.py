"""
Model download and persistence script for RAG application.

This utility script downloads the LFM2-1.2B-RAG model from Hugging Face Hub
and saves it to local storage for offline use. This is a one-time setup script
that should be run before deploying the RAG application.

Usage:
    python model_save.py

Note: This script requires internet connection and sufficient disk space (~2.5GB).
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

# Configuration: Set the local directory where the model will be saved
# Change this path based on your system's preferred model storage location
# For macOS/Linux, use forward slashes: "/Users/yourusername/models/LFM2-1.2B-RAG"
local_path = os.path.expanduser("~/models/LFM2-1.2B-RAG")  # Saves to your home directory

# Ensure the target directory exists
os.makedirs(local_path, exist_ok=True)

# Hugging Face model identifier
model_id = "LiquidAI/LFM2-1.2B-RAG"

print("Downloading model... This may take a few minutes.")

# Download tokenizer from Hugging Face Hub
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Download the language model with CPU-optimized settings
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float32,   # Use float32 for CPU compatibility
    device_map={"": "cpu"},      # Force CPU usage during download
    low_cpu_mem_usage=True       # Optimize memory usage during loading
)

# Save tokenizer and model to local directory for offline use
tokenizer.save_pretrained(local_path, safe_serialization=False)
model.save_pretrained(local_path)

print(f"✅ Model downloaded and saved to: {local_path}")
print(f"   You can now use this model offline by loading from: {local_path}")