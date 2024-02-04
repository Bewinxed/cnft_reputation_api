# this model is a representation of the NFT creator reputation

from typing import Optional
from pydantic import BaseModel, Field
from app.utils.helius import helius_client

from app.models.helius.DAS import GetAssetRequest, GetAssetRequestParams, GetAssetResponse

class CnftCreatorReputation(BaseModel):
    id: int
    reputation: int

    @classmethod
    def scan(cls, id: str):
        das = helius_client.get_asset(GetAssetRequestParams(id=id))




class CnftReputationResponse(BaseModel):
    id: str
    creators: list[CnftCreatorReputation] = Field(default_factory=list)
    reputation: int
    data: Optional[GetAssetResponse]
