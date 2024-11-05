from neo4j import GraphDatabase, Result
import re

def extract_cypher_query(text):
    # Regular expression to find the content within ```cypher ``` blocks
    match = re.search(r'```cypher\n(.*?)\n```', text, re.DOTALL)
    if match:
        return match.group(1).strip()  # Return the query without leading/trailing whitespace
    else:
        return "No Cypher query found"

def read_query(driver, ai_response, params={}):
    query = extract_cypher_query(ai_response)
    try:
        pandas_df = driver.execute_query(
            query,
            database_="neo4j",
            result_transformer_=Result.to_df
        )
        print(query)
        print(pandas_df)
        if pandas_df.empty:
            print("No result found")
            return "Either there is no result found for your question Or please help me with additional context.", query
        return pandas_df, query
    except Exception as inst:
        if "MATCH" in ai_response:
            return "Exception occurs", query
        else:
            return ai_response, query
    
