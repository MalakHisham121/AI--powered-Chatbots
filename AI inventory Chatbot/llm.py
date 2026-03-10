from llama_index.llms.groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()
 
class LLM: 
    def __init__(self):
        self.model = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
