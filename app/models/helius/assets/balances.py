from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from app.models.RPC import JsonRpcRequest

class GetAssetRequestParamsDisplayOptions(BaseModel):
    show_unverified_collections: bool = True
    show_collection_metadata: bool = True
    show_grand_total: bool = True
    show_fungible: bool = True

class GetAssetsByOwnerRequestParams(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    owner_address: str
    page: int
    limit: Optional[int] = None
    sort_by: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None
    display_options: Optional[GetAssetRequestParamsDisplayOptions] = None

class GetAssetsByOwnerRequest(JsonRpcRequest[GetAssetsByOwnerRequestParams]):
    method: str = "getAssetsByOwner"
    params: GetAssetsByOwnerRequestParams