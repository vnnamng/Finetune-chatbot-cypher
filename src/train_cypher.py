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

3. Find all the subsidaries of Apple

```
MATCH (c:Company ) - [s:SUBSIDIARY_OF] -> (o:Company) WHERE ANY (name IN c.names WHERE name = 'Apple') RETURN o
```

4. List all countries with a corporate tax rate higher than 20%

```
MATCH (c:Country) WHERE c.corporate_tax_rate > 20 RETURN c
```

5.Identify regions that contain countries with GDP greater than 1000 billion

```
MATCH (r:Region) <-[:IS_IN]- (c:Country) WHERE c.gdp > 1000 RETURN r
```

6.What are the names of companies headquartered in Asia?

```
MATCH (c:Company) -[:HEADQUARTERS_IN]-> (cn:Country ) - [:IS_IN] -> (r:Region)  WHERE r.name CONTAINS 'Asia' RETURN c.names
```

7. What are the names of companies Operating in Europe?

```
MATCH (c:Company) -[:OPERATES_IN]-> (cn:Country ) - [:IS_IN] -> (r:Region)  WHERE r.name CONTAINS 'Europe' RETURN c.names
```

8 Which companies have been founded before 2000 and operate in the United States?

```
MATCH (c:Company)-[:OPERATES_IN]->(cn :Country) WHERE ANY (aliase IN cn.aliases WHERE aliase = 'United States') AND c.founded_year < '2020' RETURN c
```

9. What companies are in Retail REITs and operates in India

```
MATCH (o:Country {name: 'India'}) <- [OPERATES_IN] - (c:Company) - [s:IS_INVOLVED_IN ] -> (x:Industry {name: 'Retail REITs'}) RETURN c
```

10. Find companies competing with Microsoft Corporation with ticker 'MSFT'

```
MATCH (c:Company {ticker: 'MSFT'}) -[:COMPETES_WITH]-> (comp) RETURN comp
```

11. Show companies with net sales over 500 million that operate in Brazil

```
MATCH (c:Company) -[o:OPERATES_IN]-> (cy:Country {name: 'Brazil'}) WHERE o.net_sales > 500 RETURN c
```

12. Which companies are headquartered in countries with a corporate tax rate less than 15%?

```
MATCH (c:Company) -[:HEADQUARTERS_IN]-> (cy:Country) WHERE cy.corporate_tax_rate < 15 RETURN c
```

13. Which Companies operate in more than 3 countries?

```
MATCH (cn:Country) <-[:OPERATES_IN]- (c:Company) WITH c, count(DISTINCT cn) AS countryCount WHERE countryCount > 3 RETURN DISTINCT c
```

14. What companies are involed in industries related to 'Software'?

```
MATCH (c:Company) -[:IS_INVOLVED_IN]-> (I:Industry) WHERE I.description CONTAINS 'Software' RETURN DISTINCT c
```

15. List all industries with companies that have no subsidiaries

```
MATCH (i:Industry) <-[:IS_INVOLVED_IN]- (c:Company) WHERE NOT (c)-[:SUBSIDIARY_OF]->() RETURN DISTINCT i
```

16. How many companies operate in the 'Telecommunication Services' sector?

```
MATCH (:Sector {name: 'Telecommunication Services'})<-[:PART_OF]-(i:Industry)<-[:IS_INVOLVED_IN]-(c:Company) RETURN COUNT(c)
```

17.Find companies that compete with those headquartered in Japan

```
MATCH (:Country {name: 'Japan'})<-[:HEADQUARTERS_IN]-(c:Company)-[:COMPETES_WITH]-(competitor:Company) RETURN DISTINCT competitor
```

18. Retrieve the top 5 industries by number of companies involved

```
MATCH (i:Industry)<-[:IS_INVOLVED_IN]-(c:Company) RETURN i, COUNT(c) AS numCompanies ORDER BY numCompanies DESC LIMIT 5
```

19. What companies have operations in more than one country?

```
MATCH (c:Company)-[:OPERATES_IN]->(cy:Country) WITH c, COUNT(cy) AS countries WHERE countries > 1 RETURN c
```

20. what are all the companies that will affect APPLE what are their relationships?

```
MATCH (c:Company) -[r:COMPETES_WITH | SUPPLIES_TO | SUBSIDIARY_OF]-> (a:Company) WHERE ANY(name IN a.names WHERE name = 'Apple') RETURN c, r
```
21. What countries does Apple operate in and what is the corporate tax rate in that country?

```
MATCH (c:Company) - [r: OPERATES_IN] - (cn:Country) WHERE ANY (name IN c.names WHERE name = 'Apple') RETURN cn.name, cn.corporate_tax_rate
```

22. What countries does Adobe operate in and what is their headcount for that country

```
MATCH (c:Company) - [r: OPERATES_IN] - (cn:Country) WHERE ANY (name IN c.names WHERE name = 'Adobe') RETURN cn, r
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