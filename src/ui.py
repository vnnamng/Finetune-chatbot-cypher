def convert_neo4j_records_to_table_format(records):
    """
    Convert the records returned by a Neo4j query to a list of dictionaries
    """
    if any(isinstance(record, str) for record in records):
        return records
    return [record.data() for record in records]

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