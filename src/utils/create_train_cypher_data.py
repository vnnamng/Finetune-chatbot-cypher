def create_train_cypher_data(nodes, relationships, relationships_direction):
    # Create a list of dictionaries containing the node properties
    node_properties = []
    for node in nodes:
        node_properties.append({
            "properties": nodes[node],
            "labels": node
        })
    # Create a list of dictionaries containing the relationships properties
    relationships_props = []
    for relationship in relationships:
        relationships_props.append({
            "source": relationships_direction[relationship][0],
            "relationship": relationship,
            "target": [relationships_direction[relationship][1]],
            "properties": relationships[relationship]
        })
    return node_properties, relationships_props

if __name__ == "__main__":
    from get_graph_schema import get_schema
    from dotenv import load_dotenv
    import os
    load_dotenv()
    host = os.getenv('HOST')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    print("Retrieving all nodes data...")
    nodes, relationships, relationships_direction = get_schema(host, user, password)
    
    node_properties, relationships_props = create_train_cypher_data(nodes, relationships, relationships_direction)
    print(node_properties)
    print(relationships_props)
