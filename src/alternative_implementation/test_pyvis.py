import pyvis
from neo4j import GraphDatabase
import neo4j
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

URI = host
AUTH = (user, password)

def main():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        visual_graph = pyvis.network.Network()

        # Query to get a graphy result
        graph_result_1 = driver.execute_query("""
            MATCH (a:Person)-[r]-(b)
            RETURN a, r, b 
LIMIT 200
            """,
            result_transformer_=neo4j.Result.graph,
        )
        
        graph_result_2 = driver.execute_query("""
            MATCH (a:Movie)-[r]-(b)
            RETURN a, r, b 
LIMIT 200
            """,
            result_transformer_=neo4j.Result.graph,
        )
        
        graph_result_3 = driver.execute_query("""
            MATCH (a:Genre)-[r]-(b)
            RETURN a, r, b 
            LIMIT 2000
            """,
            result_transformer_=neo4j.Result.graph,
        )

        # Draw graph
        nodes_text_properties = {  # what property to use as text for each node
            "Person": "name",
            "Movie": "title",
            "Genre": "name",
            "Director": "name",
            "Actor": "name",
            "User": "name",
        }
        visualize_result(visual_graph, graph_result_1, nodes_text_properties)
        visualize_result(visual_graph, graph_result_2, nodes_text_properties)
        visualize_result(visual_graph, graph_result_3, nodes_text_properties)
        visual_graph.show_buttons(filter_=['physics']) 
        visual_graph.toggle_stabilization(True)
        visual_graph.show('network.html', notebook=False)



def visualize_result(visual_graph, query_graph, nodes_text_properties):

    for node in query_graph.nodes:
        node_label = list(node.labels)[0]
        node_text = node[nodes_text_properties[node_label]]
        visual_graph.add_node(node.element_id, node_text, group=node_label)

    for relationship in query_graph.relationships:
        visual_graph.add_edge(
            relationship.start_node.element_id,
            relationship.end_node.element_id,
            title=relationship.type
        )


if __name__ == "__main__":
    main()