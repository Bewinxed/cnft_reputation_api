from typing import Optional
from pydantic import BaseModel


class Link(BaseModel):
    external_url: Optional[str] = None
    image: Optional[str] = None