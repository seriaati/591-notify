# pyright: reportOptionalMemberAccess=false

from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

import fake_useragent

from .schema import House

if TYPE_CHECKING:
    from playwright import sync_api as pw

__all__ = ("get_houses",)

ua = fake_useragent.UserAgent()


def block_ads(route: pw.Route) -> None:
    if route.request.resource_type == "image" and "ad" in route.request.url:
        route.abort()
    else:
        route.continue_()


def get_houses(playwright: pw.Playwright, *, url: str) -> list[House]:
    result: list[House] = []

    browser = playwright.chromium.launch(
        headless=True,
        proxy={
            "server": os.environ["PROXY_SERVER"],
            "username": os.environ["PROXY_USERNAME"],
            "password": os.environ["PROXY_PASSWORD"],
        },
    )
    page = browser.new_page()
    page.route("**/*", block_ads)
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")

    time.sleep(5)

    page.get_by_text("All Rights reserved.").click()
    houses = page.query_selector_all("div.houseList-item")

    for house in houses:
        price = house.query_selector(".houseList-item-price").inner_text()
        unit_price = house.query_selector(".houseList-item-unitprice").inner_text()

        title_element = house.query_selector(".houseList-item-title")
        title = title_element.inner_text()

        house_url = (
            house.query_selector(".houseList-item-title").query_selector("a").get_attribute("href")
        )
        if house_url is None:
            continue
        house_url = "https://sale.591.com.tw" + house_url

        house_id = house_url.split("/")[-1].split(".")[0]

        result.append(
            House(title=title, url=house_url, id=house_id, price=price, unit_price=unit_price)
        )

    return result
