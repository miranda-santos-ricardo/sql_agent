import os
import duckdb as db
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class SQLAgent:

   def __init__(self, api_key: str, base_url, model, tbl_name, max_token=5000):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL_ID")
        self.tbl_name = tbl_name
        self.max_token = max_token

        self.client = OpenAI(api_key=self.api_key)
        self.system = ph.system_prompt(tbl_name=tbl_name)
    
    def send_prompt(self, question):
        self.user = ph.user_prompt(question=question)
        self.response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system.system},
                {"role": "user", "content": self.user},
            ],
            max_completion_tokens=self.max_token,
        )

        content = self.response.choices[0].message.content
        if pq.is_markdown_code_chunk(text=content):
            query = pq.extract_code_from_markdown(markdown_text=content)
        else:
            query = content

        self.query = query

    def ask_question(self, question, verbose=True):
        self.send_prompt(question=question)
        self.data = db.sql(self.query)
        if verbose:
            print(self.query)
            print(self.data)