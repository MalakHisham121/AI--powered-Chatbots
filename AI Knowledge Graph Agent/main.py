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
    
    from llama_index.core.storage.chat_store import SimpleChatStore
    from llama_index.core.memory import ChatMemoryBuffer
    from llama_index.core.base.llms.types import ChatMessage

    os.makedirs("memory", exist_ok=True)
    chat_store_path = os.path.join("memory", "knowledge_chat_memory.json")
    if os.path.exists(chat_store_path):
        chat_store = SimpleChatStore.from_persist_path(chat_store_path)
    else:
        chat_store = SimpleChatStore()

    memory = ChatMemoryBuffer.from_defaults(
        chat_store=chat_store, chat_store_key="user_1", token_limit=3000
    )

    classifier = IntentClassifier(llm)
    engine = CypherEngine(graph_store)
    synthesizer = SynthesisEngine(llm)

    print("--- LlamaIndex Neo4j Agent Ready ---")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]: break

        history_msgs = memory.get_messages()
        history_str = "\n".join([f"{msg.role.value}: {msg.content}" for msg in history_msgs])

        intent_data = classifier.classify(user_input, chat_history_str=history_str)
        
        db_result = engine.execute(intent_data)
        
        final_response = synthesizer.summarize(db_result)
        
        memory.put(ChatMessage(role="user", content=user_input))
        memory.put(ChatMessage(role="assistant", content=final_response))
        chat_store.persist(chat_store_path)

        print(f"Agent: {final_response}\n")

if __name__ == "__main__":
    run_neo4j_agent()