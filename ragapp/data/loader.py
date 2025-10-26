"""
Data loader module for RAG application.

This module provides utilities for loading and filtering TATQA dataset JSON files.
It focuses on extracting text-based questions for the RAG pipeline.
"""

import json
from pathlib import Path


def load_json(file_path: Path):
    """
    Load a JSON file from the specified path.

    Args:
        file_path (Path): Path to the JSON file to load

    Returns:
        dict or list: Parsed JSON data from the file

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_text_questions(data):
    """
    Filter dataset to retain only text-based questions.

    The TATQA dataset contains questions that can be answered from text, tables, or both.
    This function filters to keep only questions where the answer comes from text paragraphs,
    which is suitable for our text-only RAG pipeline.

    Args:
        data (list): List of dataset items containing questions

    Returns:
        list: Same dataset structure with filtered questions (only answer_from="text")
    """
    for item in data:
        if "questions" in item:
            # Keep only questions where answer_from field equals "text"
            item["questions"] = [
                q for q in item["questions"] if q["answer_from"] == "text"
            ]
    return data