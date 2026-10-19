import pytest
from aura.evaluation.metrics import ndcg_at_k, recall_at_k, reciprocal_rank


def test_recall_at_k():
    assert recall_at_k(["a", "b", "c"], {"b", "c"}, 2) == 0.5


def test_reciprocal_rank():
    assert reciprocal_rank(["x", "b", "c"], {"b"}) == 0.5
    assert reciprocal_rank(["x"], {"b"}) == 0.0


def test_ndcg_perfect_ranking():
    assert ndcg_at_k(["a", "b", "x"], {"a", "b"}, 2) == pytest.approx(1.0)


def test_invalid_k_raises():
    with pytest.raises(ValueError):
        recall_at_k([], set(), 0)
