from neo4j import GraphDatabase, basic_auth
import neo4j
import pyvis
import os
def check_and_create(folder_path):
    """Create a folder if it doesn't exist; do nothing if it already exists."""
    os.makedirs(folder_path, exist_ok=True)
    
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

def draw_graph_with_pyvis(driver, queries, nodes_text_properties):
    visual_graph = pyvis.network.Network()

    # Query to get a graphy result
    for query in queries:
        try:
            graph_result = driver.execute_query(query, result_transformer_=neo4j.Result.graph)
            visualize_result(visual_graph, graph_result, nodes_text_properties)
        except Exception as e:
            print(f"Error with query: {query}")
            print(e)

    visual_graph.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.10,
                        damping=0.95
                       )

    # Save and read graph as HTML file (on Streamlit Sharing)
    print("Saving graph as HTML file")
    try:
        path = 'tmp'
        check_and_create(path)
        visual_graph.save_graph(f'{path}/pyvis_graph.html')
        print("Graph saved as HTML file at /tmp/pyvis_graph.html")
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = 'html_files'
        check_and_create(path)
        visual_graph.save_graph(f'{path}/pyvis_graph.html')
        print("Graph saved as HTML file at /html_files/pyvis_graph.html")
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    return HtmlFile



driver_test = GraphDatabase.driver(
"bolt://3.232.134.72:7687", auth=basic_auth("neo4j", "licks-mud-adherences"))
nodes_text_properties = {  # what property to use as text for each node
    "Person": "name",
    "Movie": "title",
    "Genre": "name",
    "Director": "name",
    "Actor": "name",
    "User": "name",
}

queries = ["""
    MATCH (a:Person)-[r]-(b)
    RETURN a, r, b 
LIMIT 200
    """]

HtmlFile = draw_graph_with_pyvis(driver_test, queries, nodes_text_properties)

driver_test.close()