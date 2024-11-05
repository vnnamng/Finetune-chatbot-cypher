def convert_neo4j_records_to_table_format(records):
    """
    Convert the records returned by a Neo4j query to a list of dictionaries
    """
    if any(isinstance(record, str) for record in records):
        return records
    return [record.data() for record in records]