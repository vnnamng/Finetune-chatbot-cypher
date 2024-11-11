from neo4j import GraphDatabase, Result
import re
import pandas as pd

def extract_cypher_query(text):
    """Extracts Cypher query from text within ```cypher ``` blocks."""
    match = re.search(r'```cypher\n(.*?)\n```', text, re.DOTALL)
    return match.group(1).strip() if match else None
    
def flatten_node_to_columns(record):
    """Flattens a Neo4j record, turning each Node's properties into separate columns."""
    flat_record = {}
    for key, value in record.items():
        try:
            if hasattr(value, "_properties"):  # If it's a Node, extract properties as columns
                for prop_key, prop_value in value.items():
                    flat_record[f"{key}_{prop_key}"] = prop_value
                flat_record[f"{key}_element_id"] = value.element_id
                flat_record[f"{key}_labels"] = list(value.labels)
            elif isinstance(value, (list, tuple)):
                # Flatten each node in a list or tuple
                flat_record[key] = [flatten_node_to_columns({f"{key}_{i}": item}) if hasattr(item, "_properties") else item for i, item in enumerate(value)]
            else:
                flat_record[key] = value
        except:
            continue
    return flat_record

def read_query(driver, ai_response, params={}):
    query = extract_cypher_query(ai_response)
    print(ai_response)
    if query is None:
        return "No Cypher query found in the provided text.", "", None

    try:
        # Execute the query and get raw results
        with driver.session() as session:
            raw_results = session.run(query)

            # Process records, flattening Nodes if needed
            records = []
            for record in raw_results:
                flat_record = flatten_node_to_columns(record)
                records.append(flat_record)

            # Convert to DataFrame
            pandas_df = pd.DataFrame(records)
            print("Executed Query:", query)
            print(pandas_df)

            if pandas_df.empty:
                print("No results found.")
                return "No results found for your query. Please provide additional context or check the query.", raw_results, query

            return pandas_df, raw_results, query

    except Exception as e:
        print("An error occurred:", e)
        return f"An error occurred: {e}", "", query
