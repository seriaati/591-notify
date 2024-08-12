import argparse
import pathlib
import time

from loguru import logger

from src.database import load_posts, save_posts
from src.scraper import fetch_houses
from src.utils import line_notify

parser = argparse.ArgumentParser()
parser.add_argument(
    "--token",
    type=str,
    required=True,
    help="Line Notify token",
)
args = parser.parse_args()


def main() -> None:
    logger.info("Start scraping")
    file_path = pathlib.Path("houses.json")

    houses = fetch_houses()
    logger.info(f"Found {len(houses)} houses")

    current_houses = load_posts(file_path)
    logger.info(f"Found {len(current_houses)} houses in database")

    saved_houses = save_posts(houses, current_houses, file_path)
    logger.info(f"Saved {len(saved_houses)} houses")

    for house in saved_houses:
        line_notify(f"\n發現新標的!\n{house.name}\n{house.url}", token=args.token)

    logger.info("Scraping finished")


if __name__ == "__main__":
    logger.add("log.log", rotation="1 day", retention="7 days", level="INFO")
    start = time.time()
    main()
    logger.info(f"Execution time: {time.time() - start:.2f} seconds")
