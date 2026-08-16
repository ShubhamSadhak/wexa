#!/usr/bin/env python3
import argparse, csv, json, random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dataset'/'prepared'; OUT.mkdir(parents=True,exist_ok=True)
def main():
 p=argparse.ArgumentParser(); p.add_argument('--relationships',type=int,default=100000); p.add_argument('--nodes',type=int,default=None); p.add_argument('--seed',type=int,default=42); a=p.parse_args()
 n=a.nodes or max(10000,a.relationships//8); r=random.Random(a.seed)
 with open(OUT/'nodes.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['id','value']); w.writeheader()
  for i in range(n): w.writerow({'id':i,'value':r.randint(1,100000)})
 with open(OUT/'edges.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['src','dst']); w.writeheader()
  for _ in range(a.relationships): w.writerow({'src':r.randrange(n),'dst':r.randrange(n)})
 meta={'source':'Deterministic graph-shaped benchmark fixture; replace with the selected public dataset for final submission.','node_count':n,'relationship_count':a.relationships,'load_method':'adapter-specific'}
 (ROOT/'dataset_meta.json').write_text(json.dumps(meta,indent=2))
 print(json.dumps(meta,indent=2))
if __name__=='__main__': main()
