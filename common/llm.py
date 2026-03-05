from llama_index.llms.openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
 
class LLM:
    def __init__(self):
        self.model = OpenAI(model="gpt-5-min", temperature=0, api_key=os.getenv("GROQ_API_KEY"))
