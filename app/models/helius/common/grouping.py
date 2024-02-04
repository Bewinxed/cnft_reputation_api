from pydantic import BaseModel


class Grouping(BaseModel):
    group_key: str
    group_value: str