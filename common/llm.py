from llama_index.llms.openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
 
class LLM: 
    def __init__(self):
        self.model = OpenAI(model="llama3-70b-8192", temperature=0, api_key=os.getenv("GROQ_API_KEY"))
