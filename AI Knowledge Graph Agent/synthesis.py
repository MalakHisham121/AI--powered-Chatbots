from llm import LLM

class SynthesisEngine:
    def __init__(self, llm: LLM):
        self.llm = llm

    def summarize(self, db_result):
        prompt = f"Database returned: {db_result}. Summarize this for the user naturally."
        return self.llm.complete(prompt).text