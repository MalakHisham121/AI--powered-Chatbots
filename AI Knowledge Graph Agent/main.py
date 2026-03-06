import os
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

from classifier import IntentClassifier
from cypher_engine import CypherEngine
from synthesis import SynthesisEngine

from llm import LLM

load_dotenv()

def run_neo4j_agent():
    llm = LLM().model
    graph_store = Neo4jPropertyGraphStore(
        username=os.getenv("NEO4J_USER"),
        password=os.getenv("NEO4J_PASSWORD"),
        url=os.getenv("NEO4J_URI"),
        database=os.getenv("NEO4J_DATABASE")
    )

    classifier = IntentClassifier(llm)
    engine = CypherEngine(graph_store)
    synthesizer = SynthesisEngine(llm)

    print("--- LlamaIndex Neo4j Agent Ready ---")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]: break

        intent_data = classifier.classify(user_input)
        
        db_result = engine.execute(intent_data, user_input)
        
        final_response = synthesizer.summarize(db_result)
        print(f"Agent: {final_response}\n")

if __name__ == "__main__":
    run_neo4j_agent()