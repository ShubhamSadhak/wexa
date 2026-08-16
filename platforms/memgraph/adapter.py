import os
from platforms.neo4j.adapter import Neo4jAdapter
class MemgraphAdapter(Neo4jAdapter):
    name="memgraph"
    def __init__(self): super().__init__(os.getenv("MEMGRAPH_URI"), os.getenv("MEMGRAPH_PASSWORD"), user="")
