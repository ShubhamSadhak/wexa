import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'results'; CHARTS=ROOT/'report'/'charts'; CHARTS.mkdir(parents=True,exist_ok=True)

def main():
 files=[p for p in RESULTS.glob('*.json') if p.name!='.gitkeep']
 if not files:
  print('No results found — run the benchmarks first'); return
 rows=[]; status=[]
 for p in files:
  d=json.loads(p.read_text()); status.append((d.get('platform'),d.get('error')))
  for r in d.get('records',[]): rows.append(r)
 if not rows:
  print('No measured workload results found — run the benchmarks first');
  return
 df=pd.DataFrame(rows)
 pivot=df.pivot_table(index='workload',columns='platform',values='p95_ms',aggfunc='first')
 ax=pivot.plot(kind='bar',figsize=(11,6)); ax.set_title('CognoBench p95 latency by workload'); ax.set_ylabel('Latency (ms)'); ax.set_xlabel('Workload'); ax.legend(title='Platform'); ax.tick_params(axis='x',rotation=35); fig=ax.get_figure(); fig.tight_layout(); fig.savefig(CHARTS/'p95_latency.png',dpi=160); plt.close(fig)
 lines=['# CognoBench — Generated Results','','## Results matrix','',pivot.round(3).to_markdown(),'', '## Platform status','']
 for platform,error in sorted(status): lines.append(f'- **{platform}**: FAILED — {error}' if error else f'- **{platform}**: results present')
 lines += ['', '## Methodology', '', 'Read workloads are warmed up before measurement and use the configured iteration count. Resource tiers and caveats must be verified from the actual platform instances before interpreting performance differences.', '', '![p95 latency](charts/p95_latency.png)']
 (ROOT/'report'/'README_generated.md').write_text('\n'.join(lines))
 print('Generated report/README_generated.md and report/charts/p95_latency.png')
if __name__=='__main__': main()
