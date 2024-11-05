from neo4j import GraphDatabase


URI = host
AUTH = (user, password)

def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)  # Synchronous call to run the query
        print(result)
        return [record for record in result]

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    # Example usage
    query = """
    MATCH (p:Person {name: "Stanley Kubrick"})-[r:DIRECTED]->(m:Movie)
    RETURN m.title
    """
    movies = run_query(driver, query)
    print(movies)
    for movie in movies:
        print(movie["m.title"])

    # Close the driver after use
    driver.close()


