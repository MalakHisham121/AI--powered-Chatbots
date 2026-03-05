import json
from llama_index.llms.openai import OpenAI
from prompts import CLASSIFIER_PROMPT
from common.llm import LLM

class IntentClassifier:

    def classify(self, user_text):
        response = LLM().model.complete(f"{CLASSIFIER_PROMPT}\nUser Input: {user_text}")
        return json.loads(response.text)