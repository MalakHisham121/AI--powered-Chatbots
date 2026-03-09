import json
import re
from prompts import INTENT_PROMPT, EXTRACTION_PROMPT

class IntentClassifier:
    def __init__(self, llm):
        self.llm = llm

    def _parse_json(self, text):
        """Helper to safely clean and parse LLM JSON output."""
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r'^```json\s*|```$', '', text, flags=re.MULTILINE).strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return {}

    def classify(self, user_text):
        # Step 1: Get the Intent
        intent_res = self.llm.complete(f"{INTENT_PROMPT}\nUser Input: {user_text}")
        intent_data = self._parse_json(intent_res.text)
        intent = intent_data.get("intent", "unknown")

        # Step 2: Extract details based on the intent
        extraction_prompt = EXTRACTION_PROMPT.format(intent=intent)
        extract_res = self.llm.complete(f"{extraction_prompt}\nUser Input: {user_text}")
        final_data = self._parse_json(extract_res.text)
        
        # Step 3: Combine them and return
        final_data["intent"] = intent
        return final_data