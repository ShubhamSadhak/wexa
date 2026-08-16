#!/usr/bin/env bash
set -u
PLATFORMS=(cognodb neo4j memgraph arango tigergraph)
for p in "${PLATFORMS[@]}"; do
  echo "===== $p: load ====="
  python load_data.py --platform "$p" || true
  for w in traversal_1hop traversal_2hop traversal_3hop point_lookup indexed_lookup aggregation mixed_rw; do
    echo "===== $p: $w ====="
    python run_workload.py --platform "$p" --workload "$w" || true
  done
done
python generate_report.py
