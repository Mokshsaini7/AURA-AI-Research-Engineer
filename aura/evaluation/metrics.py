import math
from collections.abc import Sequence


def recall_at_k(ranked_ids: Sequence[str], relevant_ids: set[str], k: int) -> float:
    if k < 1:
        raise ValueError("k must be at least 1")
    if not relevant_ids:
        return 0.0
    return len(set(ranked_ids[:k]) & relevant_ids) / len(relevant_ids)


def reciprocal_rank(ranked_ids: Sequence[str], relevant_ids: set[str]) -> float:
    for rank, item_id in enumerate(ranked_ids, start=1):
        if item_id in relevant_ids:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(ranked_ids: Sequence[str], relevant_ids: set[str], k: int) -> float:
    if k < 1:
        raise ValueError("k must be at least 1")
    dcg = sum(1 / math.log2(rank + 1)
              for rank, item_id in enumerate(ranked_ids[:k], start=1)
              if item_id in relevant_ids)
    ideal_hits = min(len(relevant_ids), k)
    ideal = sum(1 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    return dcg / ideal if ideal else 0.0
