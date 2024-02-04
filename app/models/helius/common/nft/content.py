from typing import List, Optional
from pydantic import BaseModel

from app.models.helius.common.file import File
from app.models.helius.common.grouping import Grouping
from app.models.helius.common.nft.compression import Compression
from app.models.helius.common.nft.creator import Creator
from app.models.helius.common.nft.royalty import Royalty
from app.models.helius.common.nft.supply import Supply
from app.models.helius.common.ownership import Ownership
from app.models.helius.common.link import Link

class NFTContent(BaseModel):
    schema: str
    json_uri: str
    files: List[File]
    metadata: dict
    links: List[Link]
    authorities: List[dict]
    compression: Compression
    grouping: List[Grouping]
    royalty: Royalty 
    creators: List[Creator]
    ownership: Ownership
    supply: Optional[Supply]
    mutable: bool
    burnt: bool