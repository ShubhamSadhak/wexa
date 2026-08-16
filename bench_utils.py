from __future__ import annotations
import json, statistics, time
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORKLOADS=['traversal_1hop','traversal_2hop','traversal_3hop','point_lookup','indexed_lookup','aggregation','mixed_rw']
def percentile(xs,p):
 if not xs: return None
 xs=sorted(xs); k=(len(xs)-1)*p; f=int(k); c=min(f+1,len(xs)-1); return xs[f]+(xs[c]-xs[f])*(k-f)
def timed(adapter,workload,iterations=100,params=None,warmup=10,concurrency=1):
 params=params or {'id':1,'value':50000}
 for _ in range(warmup): adapter.query(workload,params)
 vals=[]
 for _ in range(iterations):
  t=time.perf_counter(); adapter.query(workload,params); vals.append((time.perf_counter()-t)*1000)
 return {'platform':adapter.name,'workload':workload,'p50_ms':percentile(vals,.5),'p95_ms':percentile(vals,.95),'iterations':iterations,'concurrency':concurrency,'timestamp':datetime.now(timezone.utc).isoformat()}
def load_csv():
 import csv
 p=ROOT/'dataset'/'prepared'
 with open(p/'nodes.csv') as f: nodes=[{'id':int(x['id']),'value':int(x['value'])} for x in csv.DictReader(f)]
 with open(p/'edges.csv') as f: edges=[{'src':int(x['src']),'dst':int(x['dst'])} for x in csv.DictReader(f)]
 return nodes,edges
def write_results(platform,records,ingest=None,error=None):
 out={'platform':platform,'records':records,'ingest':ingest,'error':error}
 (ROOT/'results'/f'{platform}.json').write_text(json.dumps(out,indent=2))
 return out
