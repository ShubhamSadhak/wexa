import os, time
from arango import ArangoClient
from platforms.base import GraphAdapter, PlatformSpec
class ArangoAdapter(GraphAdapter):
    name="arango"
    def __init__(self): self.client=None; self.db=None; self.spec=PlatformSpec(self.name, driver_used="python-arango")
    def connect(self):
        uri=os.getenv("ARANGO_URI"); pwd=os.getenv("ARANGO_PASSWORD")
        if not uri or not pwd: raise RuntimeError("Missing ARANGO_URI/ARANGO_PASSWORD")
        self.client=ArangoClient(hosts=uri); self.db=self.client.db("_system", username="root", password=pwd)
    def close(self): pass
    def reset(self):
        for n in ("nodes","edges"):
            if self.db.has_collection(n): self.db.delete_collection(n)
        self.db.create_collection("nodes"); self.db.create_collection("edges", edge=True)
    def load(self,nodes,edges):
        t=time.perf_counter(); self.db.collection("nodes").insert_many(nodes); self.db.collection("edges").insert_many([{"_from":f"nodes/{e['src']}","_to":f"nodes/{e['dst']}","_key":str(i)} for i,e in enumerate(edges)]); sec=time.perf_counter()-t
        return {"seconds":sec,"nodes_per_sec":len(nodes)/sec if sec else 0,"relationships_per_sec":len(edges)/sec if sec else 0}
    def query(self,workload,params):
        q={"point_lookup":"FOR n IN nodes FILTER n._key == @id RETURN n.value","indexed_lookup":"FOR n IN nodes FILTER n.value == @value RETURN n","aggregation":"FOR n IN nodes COLLECT AGGREGATE a=AVERAGE(n.value) RETURN a"}[workload]
        return list(self.db.aql.execute(q,batch_size=1000,bind_vars=params))
    def create_indexes(self):
        self.db.collection("nodes").add_hash_index(["value"])
