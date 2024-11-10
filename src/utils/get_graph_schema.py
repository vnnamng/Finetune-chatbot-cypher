from neo4j import GraphDatabase

def get_schema(host, user, password):
    print("Connecting to the database...")
    print(host, user)

    # Initialize the driver
    driver = GraphDatabase.driver(host, auth=(user, password))
    query = """
    CALL apoc.meta.data();
    """
    with driver.session() as session:
        result = session.run(query)
        nodes = {}
        relationships = {}
        relationships_direction = {}
        for record in sorted(result, key=lambda x: x["elementType"]):
            if record["elementType"] == "node":
                if record["label"] not in nodes:
                    nodes[record["label"]] = []
                if record["type"] != "RELATIONSHIP":
                    nodes[record["label"]].append(record["property"])
                else:
                    relationships_direction[record["property"]] = (record["label"], record["other"][0])
            elif record["elementType"] == "relationship":
                if record["label"] not in relationships:
                    relationships[record["label"]] = []
                if record["property"] not in nodes:
                    relationships[record["label"]].append(record["property"])
    driver.close()
    return nodes, relationships, relationships_direction
if __name__ == "__main__":

    from dotenv import load_dotenv
    import os
    load_dotenv()
    host = os.getenv('HOST')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    print("Retrieving all nodes data...")
    nodes, relationships, relationships_direction = get_schema(host, user, password)
    print(nodes)
    print("Retrieving all relationships data...")
    print(relationships)
    print("Retrieving all relationships directions...")
    print(relationships_direction)
    
