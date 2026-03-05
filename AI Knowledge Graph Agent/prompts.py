CLASSIFIER_PROMPT = """
Classify the user input into one of these intents: 'add', 'inquire', 'edit', 'delete'.
Return ONLY a JSON object with 'intent' and 'summary' keys.
- add: Storing new facts.
- inquire: Searching for information.
- edit: Correcting existing facts.
- delete: Removing outdated/incorrect facts.
"""



CYPHER_GENERATOR_PROMPT = """
You are a Cypher query generator. Convert the user's intent into a valid Neo4j Cypher query.
Schema: (Entity {name, description})
Return ONLY the raw Cypher query string. No markdown code blocks.
"""

SYNTHESIS_PROMPT = """
You are a helpful AI assistant. The user performed an action on the knowledge graph.
Based on the database result provided, generate a natural, human-readable response 
summarizing the action or answering the query.
"""