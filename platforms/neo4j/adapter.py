import os, time
from neo4j import GraphDatabase
from platforms.base import GraphAdapter, PlatformSpec

class Neo4jAdapter(GraphAdapter):
    name = "neo4j"
    def __init__(self, uri=None, password=None, user="neo4j"):
        self.uri = uri or os.getenv("AURA_URI")
        self.password = password or os.getenv("AURA_PASSWORD")
        self.user = user
        self.driver = None
        self.spec = PlatformSpec(self.name, driver_used="neo4j")
    def connect(self):
        if not self.uri or not self.password: raise RuntimeError(f"Missing credentials for {self.name}")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        self.driver.verify_connectivity()
    def close(self):
        if self.driver: self.driver.close()
    def _run(self, cypher, params=None):
        with self.driver.session() as s: return s.run(cypher, params or {}).consume()
    def reset(self): self._run("MATCH (n) DETACH DELETE n")
    def load(self, nodes, edges):
        t=time.perf_counter()
        with self.driver.session() as s:
            s.run("UNWIND $rows AS r MERGE (n:Node {id:r.id}) SET n.value=r.value", rows=nodes).consume()
            s.run("UNWIND $rows AS r MATCH (a:Node {id:r.src}), (b:Node {id:r.dst}) MERGE (a)-[:REL]->(b)", rows=edges).consume()
        sec=time.perf_counter()-t
        return {"seconds":sec,"nodes_per_sec":len(nodes)/sec if sec else 0,"relationships_per_sec":len(edges)/sec if sec else 0}
    def query(self, workload, params):
        q={
        "traversal_1hop":"MATCH (a:Node {id:$id})-[:REL]->(b) RETURN count(b) AS n",
        "traversal_2hop":"MATCH (a:Node {id:$id})-[:REL]->()-[:REL]->(b) RETURN count(b) AS n",
        "traversal_3hop":"MATCH (a:Node {id:$id})-[:REL]->()-[:REL]->()-[:REL]->(b) RETURN count(b) AS n",
        "point_lookup":"MATCH (n:Node {id:$id}) RETURN n.value AS value",
        "indexed_lookup":"MATCH (n:Node {value:$value}) RETURN count(n) AS n",
        "aggregation":"MATCH (n:Node) RETURN avg(n.value) AS avg_value",
        "mixed_rw":"MATCH (n:Node {id:$id}) RETURN n.value AS value"}[workload]
        return self._run(q, params)
    def create_indexes(self):
        try: self._run("CREATE INDEX node_id IF NOT EXISTS FOR (n:Node) ON (n.id)")
        except Exception: pass
        try: self._run("CREATE INDEX node_value IF NOT EXISTS FOR (n:Node) ON (n.value)")
        except Exception: pass
