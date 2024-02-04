from typing import Optional
from pydantic import BaseModel


class Attribute(BaseModel):
    value: str
    trait_type: str
    max_value: Optional[int] = None
    display_type: Optional[str] = None