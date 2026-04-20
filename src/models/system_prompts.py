from dataclasses import dataclass

@dataclass
class SystemPrompt:
    system: str
    schema: str
    col_names: str
    col_types: str
    tbl_name: str

    