
import duckdb as db
from models import SystemPrompt, TableAttributes

class PromptHandler:
    def __init__(self, system_prompt = None, user_prompt = None):
        self.tbl_attr = None

    def user_prompt(self, question:str) -> str:
        user_template = f"Write a SQL query that returns: {question}"
        return user_template

    def get_tbl_attr(self, tbl_name: str) -> TableAttributes:
        """
        Get column names, types, and schema definition string for a DuckDB table.
        """

        # Query schema
        table_schema = db.sql(f"DESCRIBE SELECT * FROM {tbl_name};").df()
        col_info = table_schema[["column_name", "column_type"]]

        # Build schema string
        schema_str = ", ".join(
            f"{name} {dtype}"
            for name, dtype in zip(col_info["column_name"], col_info["column_type"])
        )
        self.tbl_attr = TableAttributes(
            col_names=col_info["column_name"].tolist(),
            col_types=col_info["column_type"].tolist(),
            tbl_schema=schema_str,
        )
        
    def system_prompt(self, tbl_name:str,additional_context:str=None) -> str:
        self.get_tbl_attr(tbl_name)
        # Prompt templates
        system_template = (
            "Given the following SQL table, your job is to write queries given a user’s request. "
            "Return just the SQL query as plain text, without additional text, and don't use markdown format.\n\n"
            f"{additional_context}"
            f"CREATE TABLE {tbl_name} ({self.tbl_attr.tbl_schema})\n"
        )
        return system_template 

    def get_character_distinct_values(self, tbl_name:str, col_name:str, num_values:int=50) -> str:
        query = f"SELECT DISTINCT {col_name} FROM {tbl_name} LIMIT {num_values};"
        result = db.sql(query).df()
        distinct_values = result[col_name].tolist()
        return f"Some distinct values for column '{col_name}' are: {distinct_values}\n"

    

    