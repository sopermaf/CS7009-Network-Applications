from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
import getpass

pw = getpass.getpass()

gdb = GraphDatabase("http://localhost:7474", username="neo4j", password=pw)

query = "MATCH p=()-[r:contributes]->() RETURN p "
results = gdb.query(query, data_contents=True)

print(results.stats)

