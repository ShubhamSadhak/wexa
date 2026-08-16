import argparse,json,os
from dotenv import load_dotenv
from platforms.factory import get_adapter
from bench_utils import timed,write_results,WORKLOADS
load_dotenv()
p=argparse.ArgumentParser(); p.add_argument('--platform',required=True); p.add_argument('--workload',required=True,choices=WORKLOADS); p.add_argument('--iterations',type=int,default=int(os.getenv('BENCHMARK_ITERATIONS','100'))); a=p.parse_args()
adapter=get_adapter(a.platform)
try:
 adapter.connect(); rec=timed(adapter,a.workload,a.iterations); path=f'results/{a.platform}.json';
 data=json.loads(open(path).read()) if __import__('pathlib').Path(path).exists() else {'platform':a.platform,'records':[]}
 data.setdefault('records',[]).append(rec); open(path,'w').write(json.dumps(data,indent=2)); print(rec)
except Exception as e:
 write_results(a.platform,[],None,str(e)); print(f'{a.platform}: FAILED — {e}')
finally:
 try: adapter.close()
 except Exception: pass
