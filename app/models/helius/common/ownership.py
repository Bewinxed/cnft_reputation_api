from typing import Optional
from pydantic import BaseModel


class Ownership(BaseModel):
    frozen: bool
    delegated: bool
    delegate: Optional[str] = None
    ownership_model: str
    owner: str