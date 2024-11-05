from utils.get_graph_schema import get_schema
from utils.create_train_cypher_data import create_train_cypher_data
from dotenv import load_dotenv
import os
load_dotenv()

host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')

examples = """
1. What are the companies in Industrial Machinery

```
MATCH (i: Industry {name: 'Industrial Machinery'}) <- [w:IS_INVOLVED_IN] - (c : Company) RETURN c
```

2. Find all sibling companies of Tesla, Inc with ticker 'TSLA'

```
MATCH (c:Company {ticker: 'TSLA'}) <-[:SUBSIDIARY_OF]- (parent) -[:SUBSIDIARY_OF]-> (sibling) RETURN sibling
```
"""

nodes, relationships, relationships_direction = get_schema(host, user, password)
node_properties, relationships_props = create_train_cypher_data(nodes, relationships, relationships_direction)

print(node_properties)
print(relationships_props)
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