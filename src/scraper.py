# type: ignore[reportOptionalMemberAccess]
from __future__ import annotations

import time
from typing import Any

import requests
from fake_useragent import UserAgent

from .schema import House

ua = UserAgent()


def request_api() -> dict[str, Any]:
    url = "https://sale.591.com.tw/home/search/list-v2"
    params = {
        "type": "2",
        "category": "1",
        "shType": "list",
        "regionid": "17",
        "metro": "238",
        "station": "4335,4337,4341,4342,4343",
        "price": "1000_1250",
        "pattern": "2",
        "label": "1",
        "firstRow": "0",
        "totalRows": "30",
        "timestamp": str(int(time.time())),
        "recom_community": "1",
    }
    headers = {
        "deviceid": "0o638nm825bkmivmtgfrqgr068",
        "x-csrf-token": "HDVfC8UwP2TzH315smtr6VGAx3Lz36RDhblWlV7j",
        "user-agent": ua.random,
        "accept": "application/json, text/javascript, */*; q=0.01",
        "referer": "https://sale.591.com.tw",
        "cookie": "webp=1; PHPSESSID=0o638nm825bkmivmtgfrqgr068; urlJumpIp=17; T591_TOKEN=0o638nm825bkmivmtgfrqgr068; _ga=GA1.3.1269950595.1723439809; _gid=GA1.3.1037545579.1723439809; _gat=1; 591_new_session=eyJpdiI6IlJuZWNZTU1PckJWemwvMVU4eGx0UXc9PSIsInZhbHVlIjoiOEs0Tk12MnpKNHRPT2k0TE5KU1Q3dWtkTW45K1dTY2dnT0FvRzJabnRReEFYSFBFM1lWc0ZERXk3VjdqdEFCY1A4bnJEWC81L0dDSHBsRExoU08yUUF1eTZ4RTFzOThKTVZUL0tiNDFmUVNrVXNkRkx2Y0RVYklvT2JiSU10UjciLCJtYWMiOiIxNDIxZDExMjAyZjcxNjRiNDU3ZjEzYjU3MzgzOGUzNWUxOTlkNjhlNDAyYThkMDhhMmMwOTk0N2U1MGYyODdiIiwidGFnIjoiIn0%3D; tw591__privacy_agree=0; _gcl_au=1.1.930892459.1723439810",
    }
    return requests.get(url, headers=headers, params=params).json()


def fetch_houses() -> list[House]:
    data = request_api()
    houses: list[House] = []
    added_names: set[str] = set()
    for house in data["data"]["house_list"]:
        name = house["title"]
        if name in added_names:
            continue
        house_id = house["houseid"]
        url = house.get(
            "event_show_url", f"https://sale.591.com.tw/home/house/detail/2/{house_id}.html"
        )
        houses.append(House(name=name, url=url))
        added_names.add(name)
    return houses
