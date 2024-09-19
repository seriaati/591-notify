from __future__ import annotations

import argparse
from typing import Final

from loguru import logger
from playwright.sync_api import sync_playwright

from src import get_houses, line_notify, load_db, save_to_db

parser = argparse.ArgumentParser(description="591 House Scraper")
parser.add_argument("--token", type=str, help="Line Notify Token")
parser.add_argument("--headless", action="store_true", help="Run in headless mode", default=False)
parser.add_argument("--url", type=str, help="591 House URL", required=True)
args = parser.parse_args()

token = args.token
headless = args.headless
url = args.url


def main() -> None:
    logger.info("Starting 591 House Scraper")

    with sync_playwright() as p:
        houses = get_houses(p, url=url, headless=args.headless)

    logger.info(f"Found {len(houses)} houses")

    current_houses = load_db(url)
    logger.info(f"Loaded {len(current_houses)} houses from database")

    saved_houses = save_to_db(url, objs_to_save=houses, current_objs=current_houses)
    logger.info(f"Saved {len(saved_houses)} new houses to database")

    for house in saved_houses:
        logger.info(f"New House: {house}")
        if token is not None:
            line_notify(token, message=house.display)

    logger.info("591 House Scraper Finished")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)

        if token is not None:
            line_notify(token, message=f"\n出錯: {e}")
