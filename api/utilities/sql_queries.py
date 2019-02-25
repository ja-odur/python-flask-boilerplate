
EXISTS = \
    """
    SELECT 1 
    FROM {table} 
    WHERE {table}.{column} = '{value}'
    AND {table}.deleted = false
    """
