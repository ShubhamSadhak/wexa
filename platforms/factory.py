from platforms.cognodb.adapter import CognoDBAdapter
from platforms.neo4j.adapter import Neo4jAdapter
from platforms.memgraph.adapter import MemgraphAdapter
from platforms.arango.adapter import ArangoAdapter
from platforms.tigergraph.adapter import TigerGraphAdapter
ADAPTERS={"cognodb":CognoDBAdapter,"neo4j":Neo4jAdapter,"memgraph":MemgraphAdapter,"arango":ArangoAdapter,"tigergraph":TigerGraphAdapter}
def get_adapter(name): return ADAPTERS[name]()
