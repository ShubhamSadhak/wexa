import os
import pyTigerGraph as tg
from platforms.base import GraphAdapter, PlatformSpec
class TigerGraphAdapter(GraphAdapter):
    name="tigergraph"
    def __init__(self): self.conn=None; self.spec=PlatformSpec(self.name, driver_used="pyTigerGraph")
    def connect(self):
        uri=os.getenv("TIGERGRAPH_URI"); token=os.getenv("TIGERGRAPH_TOKEN")
        if not uri or not token: raise RuntimeError("Missing TIGERGRAPH_URI/TIGERGRAPH_TOKEN")
        self.conn=tg.TigerGraphConnection(host=uri, graphname="graph", apiToken=token)
    def close(self): pass
    def reset(self): pass
    def load(self,nodes,edges):
        raise NotImplementedError("TigerGraph schema/loading is deployment-specific; define the graph schema and loading job for the chosen free-tier instance.")
    def query(self,workload,params): raise NotImplementedError("Add equivalent installed GSQL queries before benchmarking TigerGraph.")
    def create_indexes(self): pass
