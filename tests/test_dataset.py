from pathlib import Path

def test_structure():
 root=Path(__file__).resolve().parents[1]
 for p in ['README.md','requirements.txt','.env.example','setup.py','load_data.py','run_workload.py','generate_report.py','scripts/run_all.sh']:
  assert (root/p).exists()
