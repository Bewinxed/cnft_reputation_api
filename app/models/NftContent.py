from typing import List
from pydantic import BaseModel

from app.models.helius.DAS import Links


class NFTContent(BaseModel):
    schema: str
    json_uri: str
    files: List[File]
    metadata: dict
    links: Links
    authorities: List[dict]
    compression: Compression
    grouping: List[Grouping]
    royalty: Royalty 
    creators: List[Creator]
    ownership: Ownership
    supply: Optional[Supply]
    mutable: bool
    burnt: bool