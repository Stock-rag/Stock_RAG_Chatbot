"""
Evaluation orchestration module for RAG application.

This module provides a high-level interface for running retrieval evaluation
and displaying performance metrics. It calculates precision, recall, and MRR
(Mean Reciprocal Rank) to measure retrieval quality.
"""

from .metrics import evaluate_retrieval, calculate_mean


def run_evaluation(ground_truth, retrieval_results):
    """
    Run retrieval evaluation and display performance metrics.

    This function evaluates the quality of the retrieval system by comparing
    retrieved chunks against ground truth data. It calculates and displays
    three key metrics: Precision@k, Recall@k, and Mean Reciprocal Rank (MRR).

    Args:
        ground_truth (list[dict]): List of ground truth question dictionaries containing:
            - question (str): The question text
            - gold_chunk_ids (list[str]): List of relevant chunk IDs for this question
        retrieval_results (dict): Dictionary mapping questions to lists of retrieved chunk IDs

    Returns:
        None (prints metrics to console)

    Side Effects:
        - Prints mean precision, recall, and MRR to standard output

    Example:
        >>> gt = [{"question": "What is revenue?", "gold_chunk_ids": ["1_c0", "1_c1"]}]
        >>> results = {"What is revenue?": ["1_c0", "2_c1", "3_c0"]}
        >>> run_evaluation(gt, results)
        Mean Precision@k: 0.333
        Mean Recall@k: 0.500
        Mean MRR: 1.000

    Note:
        - Uses k=3 by default (evaluates top 3 retrieved chunks)
        - All metrics are averaged across all questions in ground_truth
    """
    # Evaluate retrieval for all questions
    all_scores = evaluate_retrieval(ground_truth, retrieval_results)

    # Calculate mean metrics across all questions
    mean_precision = calculate_mean("precision@k", all_scores)
    mean_recall = calculate_mean("recall@k", all_scores)
    mean_mrr = calculate_mean("reciprocal_rank", all_scores)

    # Display results
    print(f"Mean Precision@k: {mean_precision:.3f}")
    print(f"Mean Recall@k: {mean_recall:.3f}")
    print(f"Mean MRR: {mean_mrr:.3f}")