from pydantic import BaseModel


class File(BaseModel):
    uri: str
    cdn_uri: str 
    mime: str