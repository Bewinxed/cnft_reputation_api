from typing import Optional, TypeVar
from typing import List


from pydantic.alias_generators import to_camel

from pydantic import BaseModel, ConfigDict, validator
from typing import Generic
class JsonRpcError(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None

DataT = TypeVar('DataT', bound=BaseModel)

class JsonRpcRequest(BaseModel, Generic[DataT]):
    
    jsonrpc: str = '2.0'
    id: int = 1
    method: str
    params: Optional[DataT] = None
    
class JsonRpcResponse(BaseModel, Generic[DataT]):
    id: Optional[int] = 1
    jsonrpc: Optional[str] = "2.0"
    result: Optional[DataT] = None
    error: Optional[JsonRpcError] = None
    items: Optional[List[DataT]] = None
    
    @validator("result", "items", pre=True)
    def validate_items(cls, v):
        if isinstance(v, list):
            return cls.model_validate
        return [v]
    
class PaginatedItems(BaseModel, Generic[DataT]):
    items: List[DataT]
    total: int
    limit: int
    page: int
    