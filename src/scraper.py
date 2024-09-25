# pyright: reportOptionalMemberAccess=false

from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

from loguru import logger

from .schema import House

if TYPE_CHECKING:
    from playwright import sync_api as pw

__all__ = ("get_houses",)


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
    page.goto(url)

    added_house_ids = set()
    added_house_titles = set()

    while True:
        page.wait_for_load_state("networkidle")
        page.get_by_text("All Rights reserved.").click()

        houses = page.query_selector_all("div.houseList-item")

        for house in houses:
            try:
                price = house.query_selector(".houseList-item-price").inner_text().strip()
                unit_price = house.query_selector(".houseList-item-unitprice").inner_text().strip()

                title_element = house.query_selector(".houseList-item-title")
                title = title_element.inner_text().strip()

                house_url = (
                    house.query_selector(".houseList-item-title")
                    .query_selector("a")
                    .get_attribute("href")
                )
                if house_url is None:
                    continue
                house_url = "https://sale.591.com.tw" + house_url

                house_id = house_url.split("/")[-1].split(".")[0]
            except AttributeError:
                continue

            if house_id in added_house_ids or title in added_house_titles:
                continue

            result.append(
                House(title=title, url=house_url, id=house_id, price=price, unit_price=unit_price)
            )
            added_house_ids.add(house_id)
            added_house_titles.add(title)

        next_a = page.query_selector("a.pageNext")
        next_span = page.query_selector("span:has-text('下一頁')")

        if next_a is None:
            logger.info("Cannot find next button, stopping")
            break

        if "last" in (next_a.get_attribute("class") or ""):
            logger.info("Last page reached, stopping")
            break

        try:
            logger.info("Navigating to next page")
            time.sleep(5)
            next_span.click()
        except Exception as e:
            logger.error(f"Error clicking next button: {e}")
            break

    return result
