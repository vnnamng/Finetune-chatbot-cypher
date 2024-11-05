from utils.get_graph_schema import get_schema
from utils.create_train_cypher_data import create_train_cypher_data
from dotenv import load_dotenv
import os
load_dotenv()

host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')

examples = """
1. To find who acted in a movie:
```
MATCH (p:Person)-[r:ACTED_IN]->(m:Movie {{title: "Movie Title"}})
RETURN p.name, r.role
```

2. To find who directed a movie:
```
MATCH (p:Person)-[r:DIRECTED]->(m:Movie {{title: "Movie Title"}})
RETURN p.name
```
"""

nodes, relationships, relationships_direction = get_schema(host, user, password)
node_properties, relationships_props = create_train_cypher_data(nodes, relationships, relationships_direction)
# node_properties = """
# [
#     {
#         "properties": [
#             "part_id",
#             "supplier_id",
#             "part_name",
#             "part_description",
#             "alternate_part_id"
#         ],
#         "labels": "parts"
#     },
#     {
#         "properties": [
#             "supplier_id",
#             "part_cost",
#             "transportation_cost",
#             "labour_cost",
#             "total_cost"
#         ],
#         "labels": "cost"
#     },
#     {
#         "properties": [
#             "supplier_id",
#             "supplier_name",
#             "location"
#         ],
#         "labels": "suppliers"
#     }
# ]
# """

# relationships_props = """
# [
#     {
#         "source": "parts",
#         "relationship": "ALTERNATE_OF",
#         "target": [
#             "parts"
#         ]
#     },
#     {
#         "source": "parts",
#         "relationship": "SUPPLIED_BY",
#         "target": [
#             "suppliers"
#         ]
#     },
#     {
#         "source": "suppliers",
#         "relationship": "HAS",
#         "target": [
#             "cost"
#         ]
#     }
# ]
# """