# ANNRecallBench — measured local run

Small authored HNSW-style graph over synthetic random vectors. Build uses exact neighbour selection; no optimized HNSW library or large-scale claim.

## Results

```json
{
  "build_seconds": 0.008779300027526915,
  "operating_points": [
    {
      "ef": 10,
      "recall_at_5": 0.8550000000000001,
      "query_seconds": 0.0217482999432832
    },
    {
      "ef": 30,
      "recall_at_5": 0.99,
      "query_seconds": 0.03328249999321997
    },
    {
      "ef": 80,
      "recall_at_5": 1.0,
      "query_seconds": 0.04797840001992881
    }
  ],
  "vector_bytes": 57600,
  "directed_graph_edges": 5274,
  "checks": [
    "Query returns bounded five neighbours",
    "Measured recall within bounds"
  ],
  "scope": "Small authored HNSW-style graph over synthetic random vectors. Build uses exact neighbour selection; no optimized HNSW library or large-scale claim."
}
```

Local experiment assertions passed. This does not establish production readiness or performance on real customer data. Source fingerprints and dependency versions are in results.json.
