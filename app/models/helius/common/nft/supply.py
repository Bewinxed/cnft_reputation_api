from typing import Optional
from pydantic import BaseModel


class Supply(BaseModel):
    print_max_supply: Optional[int] = 0
    print_current_supply: Optional[int] = 0
    edition_nonce: Optional[int] = None