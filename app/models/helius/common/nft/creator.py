from pydantic import BaseModel


class Creator(BaseModel):
    address: str 
    share: int
    verified: bool