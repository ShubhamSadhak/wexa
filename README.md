# CognoBench

A fair, automated, reproducible benchmark of CognoDB Cloud against Neo4j AuraDB, Memgraph, ArangoDB and TigerGraph.

> Benchmark harness based on the supplied CognoBench planning documents. Actual performance numbers are intentionally not fabricated: they appear only after credentials, platform instances and a real dataset are supplied.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python dataset/prepare_dataset.py --relationships 100000
python setup.py
./scripts/run_all.sh
python generate_report.py
```

On Windows, run the equivalent Python commands manually or through Git Bash/WSL.

## Required workloads

- ingest throughput
- 1/2/3-hop traversal latency
- point lookup latency
- indexed lookup latency
- aggregation latency
- mixed read/write throughput

Read workloads warm up first and default to 100 measured iterations. Results are written to `results/<platform>.json` and charts to `report/charts/`.

## Platforms

`cognodb`, `neo4j`, `memgraph`, `arango`, `tigergraph`.

The adapters share one interface and keep credentials in environment variables only. See `platforms/base.py`.

## Fairness

Record equivalent vCPU/RAM/disk/tier/region information in `platform_specs.json`. Do not compare paid/enterprise tiers or multi-node deployments. Document throttling, timeouts and query-language differences in `caveats.json`.

## Dataset

`dataset/prepare_dataset.py` creates a deterministic public-style graph-shaped benchmark dataset for harness development. For the final Wexa submission, replace it with the selected public dataset and record its source in `dataset_meta.json`.

## Result schema

Each platform result contains workload records with `p50_ms`, `p95_ms`, `iterations`, `concurrency` and ISO timestamp fields, plus ingest throughput metadata.

## Single-platform debugging

```bash
python load_data.py --platform cognodb
python run_workload.py --platform cognodb --workload traversal_1hop
```

## Report

```bash
python generate_report.py
```

If no result files exist, the generator exits cleanly with `No results found — run the benchmarks first`.
