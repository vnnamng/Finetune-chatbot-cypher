from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

driver = GraphDatabase.driver(host, auth=(user, password))

query = """
MATCH (n)-[r]->(c) RETURN * LIMIT 20
"""

results = driver.session().run(query)
G = nx.MultiDiGraph()
movie_labels = {}
person_labels = {}
nodes = list(results.graph()._nodes.values())

for node in nodes:
    if 'name' in node._properties:
        person_labels[node.id] = node._properties.get('name', node.id)
    elif 'title' in node._properties:
        movie_labels[node.id] = node._properties.get('title', node.id)
    G.add_node(node.id, labels=node._labels, properties=node._properties)

rels = list(results.graph()._relationships.values())
for rel in rels:
    G.add_edge(rel.start_node.id, rel.end_node.id, key=rel.id, type=rel.type, properties=rel._properties)
    
pos = nx.spring_layout(G, seed=3068)  # Seed layout for reproducibility
options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9}
nx.draw_networkx_labels(G, pos, person_labels, font_size=5, font_color="black")
nx.draw_networkx_nodes(G, pos, nodelist=person_labels.keys(), node_color="tab:red", **options)
nx.draw_networkx_labels(G, pos, movie_labels, font_size=5, font_color="black")
nx.draw_networkx_nodes(G, pos, nodelist=movie_labels.keys(), node_color="tab:blue", **options)
nx.draw_networkx_edges(
    G,
    pos,
    width=2,
    edge_color="tab:blue",
)
plt.show()