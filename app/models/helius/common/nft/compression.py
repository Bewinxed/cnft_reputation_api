from typing import Optional
from pydantic import BaseModel

class Compression(BaseModel):
    eligible: bool
    compressed: bool
    data_hash: Optional[str] = ""
    creator_hash: Optional[str] = ""
    asset_hash: Optional[str] = ""
    tree: Optional[str] = ""
    seq: Optional[int] = 0
    leaf_id: Optional[int] = 0
