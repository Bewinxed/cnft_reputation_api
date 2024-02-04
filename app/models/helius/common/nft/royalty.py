from typing import Optional
from pydantic import BaseModel


class Royalty(BaseModel):
    royalty_model: str
    target: Optional[str] = None
    percent: float 
    basis_points: int
    primary_sale_happened: bool 
    locked: bool