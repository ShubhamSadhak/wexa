import os, sys
from pathlib import Path
from dotenv import load_dotenv
from platforms.factory import ADAPTERS
ROOT=Path(__file__).resolve().parent
load_dotenv(ROOT/'.env')
required={'cognodb':['COGNODB_URI','COGNODB_PASSWORD'],'neo4j':['AURA_URI','AURA_PASSWORD'],'memgraph':['MEMGRAPH_URI','MEMGRAPH_PASSWORD'],'arango':['ARANGO_URI','ARANGO_PASSWORD'],'tigergraph':['TIGERGRAPH_URI','TIGERGRAPH_TOKEN']}
for name,vars_ in required.items():
 missing=[v for v in vars_ if not os.getenv(v)]
 print(f'{name}: MISSING {", ".join(missing)}' if missing else f'{name}: credentials present')
try:
 import pandas, matplotlib, neo4j
 print('Core dependencies: OK')
except ImportError as e: print(f'Core dependency missing: {e}'); sys.exit(1)
