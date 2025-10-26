"""
Data preparation module for RAG application.

This module transforms the nested TATQA dataset structure into flattened lists
of paragraphs and questions with consistent IDs for retrieval and evaluation.
"""


def process_paragraphs_and_questions(train_data):
    """
    Extract and flatten paragraphs and questions from TATQA dataset.

    The TATQA dataset is structured as a list of items, where each item contains
    multiple paragraphs and questions. This function flattens the structure and
    creates unique IDs that link questions to their relevant paragraphs.

    Args:
        train_data (list[dict]): List of TATQA dataset items, each containing:
            - paragraphs (list): List of paragraph objects with 'order' field
            - questions (list): List of question objects with 'rel_paragraphs' field

    Returns:
        tuple: A tuple containing two lists:
            - all_paragraphs (list[dict]): Flattened list of paragraphs with added 'id' field
            - all_questions (list[dict]): Flattened list of questions with updated 'rel_paragraphs' IDs

    Example:
        >>> data = [{"paragraphs": [{"order": 1, "text": "..."}],
        ...          "questions": [{"rel_paragraphs": [1], "question": "..."}]}]
        >>> paras, qs = process_paragraphs_and_questions(data)
        >>> paras[0]["id"]
        "0_1"
    """
    all_paragraphs, all_questions = [], []

    # Iterate through each item in the dataset
    for idx, item in enumerate(train_data):
        # Process paragraphs: assign unique IDs based on item index and paragraph order
        if "paragraphs" in item:
            for para in item["paragraphs"]:
                # Create unique ID format: "{item_index}_{paragraph_order}"
                para["id"] = f"{idx}_{para['order']}"
                all_paragraphs.append(para)

        # Process questions: update paragraph references to match new ID format
        if "questions" in item:
            for question in item["questions"]:
                # Transform paragraph IDs to match the new format
                modified_id = [f"{idx}_{pid}" for pid in question["rel_paragraphs"]]
                question["rel_paragraphs"] = modified_id
                all_questions.append(question)

    return all_paragraphs, all_questions