import pyvis
import neo4j
import os

def check_and_create(folder_path):
    """Create a folder if it doesn't exist; do nothing if it already exists."""
    os.makedirs(folder_path, exist_ok=True)

def reorder_columns(response):
    columns = response.columns
    name_columns = [col for col in columns if "name" in col]
    non_list_columns = [col for col in columns if col not in name_columns and not isinstance(response[col].iloc[0], list)]
    list_columns = [col for col in columns if isinstance(response[col].iloc[0], list)]

    # Sort each category
    name_columns_sorted = sorted(name_columns)
    non_list_columns_sorted = sorted(non_list_columns)
    list_columns_sorted = sorted(list_columns)

    # Combine in the desired order
    column_order = name_columns_sorted + non_list_columns_sorted + list_columns_sorted
    
    return column_order

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

def draw_graph_with_pyvis(driver, queries, nodes_text_properties, custom_html_name):
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
    try:
        path = 'tmp'
        check_and_create(path)
        visual_graph.save_graph(f'{path}/{custom_html_name}.html')
        HtmlFile = open(f'{path}/{custom_html_name}.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = 'html_files'
        check_and_create(path)
        visual_graph.save_graph(f'{path}/{custom_html_name}.html')
        HtmlFile = open(f'{path}/{custom_html_name}.html', 'r', encoding='utf-8')
        
    return HtmlFile, path


