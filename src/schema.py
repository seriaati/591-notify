from pydantic import BaseModel


class House(BaseModel):
    name: str
    url: str
