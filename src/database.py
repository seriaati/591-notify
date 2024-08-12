from __future__ import annotations

import json
from typing import TYPE_CHECKING

from .schema import House

if TYPE_CHECKING:
    import pathlib


def load_posts(file_path: pathlib.Path) -> list[House]:
    if not file_path.exists():
        return []
    with open(file_path, encoding="utf-8") as f:
        return [House(**post) for post in json.load(f)]


def get_post(houses: list[House], url: str) -> House | None:
    for house in houses:
        if house.url == url:
            return house
    return None


def save_posts(
    houses_to_save: list[House], current_houses: list[House], file_path: pathlib.Path
) -> list[House]:
    houses_to_save = [post for post in houses_to_save if get_post(current_houses, post.url) is None]
    current_houses.extend(houses_to_save)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([house.model_dump() for house in current_houses], f, ensure_ascii=False, indent=2)

    return houses_to_save
