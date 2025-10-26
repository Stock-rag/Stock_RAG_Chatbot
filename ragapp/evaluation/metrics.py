"""
Retrieval evaluation metrics for RAG application.

This module implements standard information retrieval metrics including
Precision@k, Recall@k, and Mean Reciprocal Rank (MRR) to evaluate the
quality of the retrieval system.
"""


def evaluate_retrieval(ground_truth, retrieval_results, k=3):
    """
    Evaluate retrieval performance for multiple questions.

    This function calculates precision, recall, and reciprocal rank for each
    question by comparing retrieved chunks against ground truth relevant chunks.

    Args:
        ground_truth (list[dict]): List of ground truth dictionaries containing:
            - question (str): The question text
            - gold_chunk_ids (list[str]): List of relevant chunk IDs
        retrieval_results (dict): Dictionary mapping questions to lists of retrieved chunk IDs
        k (int): Number of top results to consider (default: 3)

    Returns:
        list[dict]: List of score dictionaries, one per question, containing:
            - question (str): The question text
            - precision@k (float): Precision at k (relevant retrieved / k)
            - recall@k (float): Recall at k (relevant retrieved / total relevant)
            - retrieved (list[str]): Top k retrieved chunk IDs
            - reciprocal_rank (float): Reciprocal rank of first relevant result

    Example:
        >>> gt = [{"question": "Q1", "gold_chunk_ids": ["1_c0", "1_c1"]}]
        >>> results = {"Q1": ["1_c0", "2_c0", "3_c0"]}
        >>> scores = evaluate_retrieval(gt, results, k=3)
        >>> scores[0]["precision@k"]
        0.333  # 1 relevant out of 3 retrieved

    Metrics Explained:
        - Precision@k: Fraction of retrieved chunks that are relevant
        - Recall@k: Fraction of relevant chunks that were retrieved
        - Reciprocal Rank: 1 / (rank of first relevant result)
    """
    scores = []
    for gt in ground_truth:
        q = gt["question"]
        gold_chunks = set(gt["gold_chunk_ids"])  # Relevant chunks for this question
        retrieved = retrieval_results.get(q, [])[:k]  # Top k retrieved chunks

        # Count how many retrieved chunks are relevant
        relevant_retrieved = len([c for c in retrieved if c in gold_chunks])

        # Precision@k: What fraction of retrieved results are relevant?
        precision = relevant_retrieved / len(retrieved) if retrieved else 0.0

        # Recall@k: What fraction of relevant chunks did we retrieve?
        recall = relevant_retrieved / len(gold_chunks) if gold_chunks else 0.0

        # Reciprocal Rank: 1 / (position of first relevant result)
        # Higher is better, rewards having relevant results early
        rr = 0.0
        for rank, c in enumerate(retrieved, start=1):
            if c in gold_chunks:
                rr = 1.0 / rank  # Found first relevant result at this rank
                break

        scores.append({
            "question": q,
            "precision@k": precision,
            "recall@k": recall,
            "retrieved": retrieved,
            "reciprocal_rank": rr,
        })
    return scores


def calculate_mean(key, scores):
    """
    Calculate the mean value for a specific metric across all questions.

    This helper function computes the average of a specific metric
    (like precision, recall, or MRR) across all evaluation scores.

    Args:
        key (str): The metric key to average (e.g., "precision@k", "recall@k", "reciprocal_rank")
        scores (list[dict]): List of score dictionaries from evaluate_retrieval()

    Returns:
        float: Mean value of the specified metric

    Example:
        >>> scores = [
        ...     {"precision@k": 0.5, "recall@k": 0.3},
        ...     {"precision@k": 0.7, "recall@k": 0.4}
        ... ]
        >>> calculate_mean("precision@k", scores)
        0.6

    Note:
        - Returns 0 if scores list is empty (division by zero protection)
    """
    return sum(s[key] for s in scores) / len(scores) if scores else 0.0