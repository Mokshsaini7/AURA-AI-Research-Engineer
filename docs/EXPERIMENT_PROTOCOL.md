# Experiment protocol

1. Freeze a dataset version and record its checksum.
2. Split queries into development and held-out test sets.
3. Record model version, chunk settings, top-k, software versions, GPU, and batch size.
4. Run all retrieval variants against the same corpus and queries.
5. Report Recall@k, MRR, nDCG@k, latency percentiles, and index build time.
6. Preserve per-query raw results.
7. Inspect failure cases and report trade-offs.
8. Do not tune on the held-out test set or claim unmeasured improvements.
