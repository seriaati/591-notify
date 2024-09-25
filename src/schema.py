from __future__ import annotations

from pydantic import BaseModel

__all__ = ("House",)


class House(BaseModel):
    title: str
    url: str
    id: str
    unit_price: str

    @property
    def display(self) -> str:
        return f"\n{self.title}\n價格: {self.unit_price}\n\n{self.url}"
