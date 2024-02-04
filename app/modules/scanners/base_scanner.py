from pydantic import BaseModel


class Scanner(BaseModel):
    async def scan(self):
        pass