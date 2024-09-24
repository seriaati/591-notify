from __future__ import annotations

import os

from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import sync_playwright

from src import get_houses, line_notify, load_db, save_to_db

load_dotenv()

token = os.getenv("LINE_NOTIFY_TOKEN")
url = os.environ["URL"]


def main() -> None:
    logger.info("Starting 591 House Scraper")
    logger.info(f"URL: {url}")

    with sync_playwright() as p:
        houses = get_houses(p, url=url)

    logger.info(f"Found {len(houses)} houses")

    current_houses = load_db()
    logger.info(f"Loaded {len(current_houses)} houses from database")

    saved_houses = save_to_db(objs_to_save=houses, current_objs=current_houses)
    logger.info(f"Saved {len(saved_houses)} new houses to database")

    if not current_houses:
        logger.info("First run, no notification sent")
    else:
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
