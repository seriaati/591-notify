from __future__ import annotations

import json
import pathlib

from .schema import House

__all__ = ("load_db", "save_to_db")

DB_PATH = pathlib.Path("./houses.json")


def load_db() -> list[House]:
    if not DB_PATH.exists():
        return []

    with DB_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
        return [House(**obj) for obj in data]


def save_to_db(objs_to_save: list[House], current_objs: list[House]) -> list[House]:
    current_obj_ids = {obj.id for obj in current_objs}
    current_obj_titles = {obj.title for obj in current_objs}

    objs_to_save = [
        obj
        for obj in objs_to_save
        if obj.id not in current_obj_ids and obj.title not in current_obj_titles
    ]
    current_objs.extend(objs_to_save)

    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump([obj.model_dump() for obj in current_objs], f, ensure_ascii=False, indent=2)

    return objs_to_save
