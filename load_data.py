import argparse
from dotenv import load_dotenv
from platforms.factory import get_adapter
from bench_utils import load_csv,write_results
load_dotenv()
p=argparse.ArgumentParser(); p.add_argument('--platform',required=True); a=p.parse_args()
adapter=get_adapter(a.platform)
try:
 nodes,edges=load_csv(); adapter.connect(); adapter.reset(); stats=adapter.load(nodes,edges); adapter.create_indexes(); write_results(a.platform,[],stats); print(stats)
except Exception as e:
 write_results(a.platform,[],None,str(e)); print(f'{a.platform}: FAILED — {e}')
finally:
 try: adapter.close()
 except Exception: pass
