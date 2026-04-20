
import duckdb as db
from models import SystemPrompt, TableAttributes

class PromptHandler:
    def __init__(self, system_prompt, user_prompt):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.tbl_attr = None

    def user_prompt(question:str) -> str:
        user_template = f"Write a SQL query that returns: {question}"
        return user_template

    def get_tbl_attr(tbl_name: str) -> TableAttributes:
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
        
    def system_prompt(tbl_name:str) -> str:
        self.get_tbl_attr(tbl_name)
        # Prompt templates
        system_template = (
            "Given the following SQL table, your job is to write queries given a user’s request. "
            "Return just the SQL query as plain text, without additional text, and don't use markdown format.\n\n"
            f"CREATE TABLE {tbl_name} ({self.tbl_attr.tbl_schema})\n"
        )
        return SystemPrompt(
            system=system_template,
            schema=self.tbl_attr.tbl_schema,
            col_names=self.tbl_attr.col_names,
            col_types=self.tbl_attr.col_types,
            tbl_name=tbl_name,
        ) 

    

    