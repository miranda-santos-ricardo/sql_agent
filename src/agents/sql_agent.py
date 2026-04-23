import os
import duckdb as db
from openai import OpenAI
from dotenv import load_dotenv
from utils.prompt_handler import PromptHandler
from utils.parse_query import ParseQuery

load_dotenv()

class SQLAgent:

    def __init__(self, tbl_name, max_token=5000):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL_ID")
        self.tbl_name = tbl_name
        self.max_token = max_token
        self.query = None

        #Objects
        self.ph = PromptHandler()
        self.pq = ParseQuery()
        self.client = OpenAI(api_key=self.api_key)
        #self.system = ph.system_prompt(tbl_name=tbl_name)
    
    def send_prompt(self, question):
        self.response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.ph.system_prompt(tbl_name=self.tbl_name)},
                {"role": "user", "content": self.ph.user_prompt(question=question)},
            ],
            max_completion_tokens=self.max_token,
        )

        content = self.response.choices[0].message.content

        if self.pq.is_markdown_code_chunk(text=content):
            query = self.pq.extract_code_from_markdown(markdown_text=f"{content}")
        else:
            query = content

        self.query = query

    def ask_question(self, question, verbose=True):
        self.send_prompt(question=question)
        self.data = db.sql(self.query)
        if verbose:
            print(self.query)
            print(self.data)