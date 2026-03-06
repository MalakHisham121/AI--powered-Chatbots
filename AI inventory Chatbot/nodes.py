import sqlite3
from langchain_openai import OpenAI
from state import State
from prompts import GENERATE_SQL_QUERY_PROMPT , CORRECTOR_PROMPT, RESPOND_PROMPT
from common.llm import LLM




db_name = 'inventory.db'

llm =  LLM.model
def generate(state: State)-> State:
    prompt = GENERATE_SQL_QUERY_PROMPT.format(question=state['question'], db_schema="{db_schema}")
    sql_query = llm(prompt)
    state['sql_query'] = sql_query
    return state


def correct(state: State)-> State:
    
    prompt = CORRECTOR_PROMPT.format(state=state)
    
    raw_response = llm.invoke(prompt)
    fixed_query = clean_sql(raw_response)
    
    updates = {
        "sql_query": fixed_query,
        "error": ""
    }
    return updates
     

def execute(state: State)-> State:
    query = state["sql_query"]
    execution_results = []
    error_found = ""
    
    try:
        connection = sqlite3.connect("inventory.db")
        connection.row_factory = sqlite3.Row 
        cursor = connection.cursor()
        
        cursor.execute(query)
        rows = cursor.fetchall()
        execution_results = [dict(row) for row in rows]
        
        connection.close()
    except Exception as e:
        error_found = str(e)
    
    updates = {
        "sql_result": execution_results, 
        "error": error_found
    }
    return updates  

def respond(state: State)-> State:
    results = state["sql_result"]
    question = state["question"]
    
    prompt = RESPOND_PROMPT.format(question=question, data=results)
    
    final_output = llm.invoke(prompt)
    
    updates = {"response": final_output.strip()}
    return updates

    


def clean_sql(text: str) -> str:
    cleaned = text.replace("```sql", "").replace("```", "").strip()
    return cleaned