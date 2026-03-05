GENERATE_SQL_QUERY_PROMPT = """
You are an assistant for an inventory management system. Your task is to generate SQL queries based on the user's question {question}. and searching into database and its schema is {db_schema} give only the SQL query without any explanation or text."""

CORRECTOR_PROMPT = """The query {state['sql_query']} failed with error: {state['error']}.
    Provide ONLY the corrected SQL query. Do not use markdown fences. or inform that cannot find suitable one."""



RESPOND_PROMPT = '''User asked: {question}. Database returned: {data}. Answer clearly.'''