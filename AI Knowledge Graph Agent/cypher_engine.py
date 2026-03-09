from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.graph_stores.types import EntityNode, Relation

class CypherEngine:
    def __init__(self, graph_store: Neo4jPropertyGraphStore):
        self.graph_store = graph_store

    def execute(self, intent_data):
        intent = intent_data.get('intent')
        
        if intent == "add":
            return self.add_fact(intent_data)
        elif intent == "inquire":
            return self.inquire_fact(intent_data)
        elif intent == "edit":
            return self.edit_property(intent_data)
        elif intent == "delete":
            return self.delete_fact(intent_data)
        
        return "Unknown intent."

    def add_fact(self, data):
        entity = data.get('entity', 'Unknown_Entity')
        value = data.get('value', 'Unknown_Value')
        relation = data.get('relation', 'related_to')

        query = f"""
        MERGE (n:Entity {{name: '{entity}'}})
        MERGE (m:Value {{name: '{value}'}})
        MERGE (n)-[r:`{relation}`]->(m)
        """
        
        self.graph_store.structured_query(query)
    
        return f"Created relationship: {data['entity']} --({data['relation']})--> {data['value']}"

    def inquire_fact(self, data):
        query = f"MATCH (n {{name: '{data['entity']}'}})-[r]->(m) RETURN n.name, type(r), m.name"
        return self.graph_store.structured_query(query)

    def edit_property(self, data):
        entity = data.get('entity', '').replace("'", "\\'")
        relation = data.get('relation', '').replace("'", "\\'")
        new_value = data.get('value', '').replace("'", "\\'")

        # Matches the exact entity and relation, ignoring case, and updates the value node
        query = f"""
        MATCH (n:Entity)-[r]->(m:Value) 
        WHERE toLower(n.name) = toLower('{entity}') 
          AND toLower(type(r)) = toLower('{relation}')
        SET m.name = '{new_value}'
        """
        
        self.graph_store.structured_query(query)
        return f"Updated relation '{relation}' for '{entity}' to '{new_value}'."

    def delete_fact(self, data):
        entity = data.get('entity', '').replace("'", "\\'")
        relation = data.get('relation', '').replace("'", "\\'")

        if relation:
            # Delete the specific relation and value node, then check if entity is orphaned
            query = f"""
            MATCH (n:Entity)-[r]->(m:Value)
            WHERE toLower(n.name) = toLower('{entity}') 
              AND toLower(type(r)) = toLower('{relation}')
            
            // Delete the relationship and the target value node
            DELETE r
            DETACH DELETE m
            
            // Check if the entity node has any other relationships left
            WITH n
            OPTIONAL MATCH (n)-[other_r]-()
            WITH n, count(other_r) AS rel_count
            
            // If the relationship count is 0, delete the main entity node too
            FOREACH (ignore IN CASE WHEN rel_count = 0 THEN [1] ELSE [] END | DETACH DELETE n)
            """
            self.graph_store.structured_query(query)
            return f"Deleted relation '{relation}' and value for '{entity}'."
            
        else:
            # Fallback: Delete entire entity if no relation was specified
            query = f"""
            MATCH (n:Entity) 
            WHERE toLower(n.name) = toLower('{entity}') 
            DETACH DELETE n
            """
            self.graph_store.structured_query(query)
            return f"Deleted entire entity '{entity}' from the graph."