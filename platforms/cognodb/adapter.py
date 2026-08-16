import os
from neo4j import GraphDatabase
from platforms.neo4j.adapter import Neo4jAdapter

class CognoDBAdapter(Neo4jAdapter):
    name = "cognodb"
    def __init__(self):
        super().__init__(os.getenv("COGNODB_URI"), os.getenv("COGNODB_PASSWORD"), user="cognodb")
