from dataclasses import dataclass

@dataclass
class TableAttributes:
    col_names: list[str]
    col_types: list[str]
    tbl__schema: str 


    