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
        subj = EntityNode(name=data['subject'], label="Entity")
        obj = EntityNode(name=data['object'], label="Entity")
        rel = Relation(label=data['relation'], source_id=subj.id, target_id=obj.id)
        
        self.graph_store.upsert_nodes([subj, obj])
        self.graph_store.upsert_relations([rel])
        return f"Created relationship: {data['subject']} --({data['relation']})--> {data['object']}"

    def inquire_fact(self, data):
        query = f"MATCH (n {{name: '{data['subject']}'}})-[r]->(m) RETURN n.name, type(r), m.name"
        return self.graph_store.structured_query(query)

    def edit_property(self, data):
        query = f"MATCH (n {{name: '{data['subject']}'}}) SET n.{data['property_key']} = '{data['property_value']}'"
        self.graph_store.structured_query(query)
        return f"Updated {data['property_key']} for {data['subject']} to {data['property_value']}."

    def delete_fact(self, data):
        query = f"MATCH (n {{name: '{data['subject']}'}}) DETACH DELETE n"
        self.graph_store.structured_query(query)
        return f"Deleted entity {data['subject']} from the graph."