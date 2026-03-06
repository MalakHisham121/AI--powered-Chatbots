import json
from llama_index.llms.groq import Groq
from prompts import CLASSIFIER_PROMPT
from llm import LLM

class IntentClassifier:
    def __init__(self, llm):
        self.llm = llm

    def classify(self, user_text):
        response = LLM().model.complete(f"{CLASSIFIER_PROMPT}\nUser Input: {user_text}")
        return json.loads(response.text)