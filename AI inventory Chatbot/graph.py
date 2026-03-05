
from langchain_openai import OpenAI
from langgraph.graph import END
from state import State
from nodes import generate, execute, corrector, respond
from langgraph import StateGraph



def router(state: State):
    if state.get("error"):
        return "corrector"
    return "responder"

workflow = StateGraph(State)

workflow.add_node("generator", generate)
workflow.add_node("executor", execute)
workflow.add_node("corrector", corrector)
workflow.add_node("responder", respond)

workflow.set_entry_point("generator")
workflow.add_edge("generator", "executor")

workflow.add_conditional_edges(
    "executor",
    router,
    {
        "corrector": "corrector",
        "responder": "responder"
    }
)

workflow.add_edge("corrector", "executor")
workflow.add_edge("responder", END)

app = workflow.compile()




