import asyncio
import logging
from app.scraper import discover_articles
from app.keyword_store import list_active_keywords
from app.service import process_article
from app.config import NEWS_SOURCES, SCRAPE_INTERVAL_SECONDS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def run_scraper_loop():
    seen_urls: set[str] = set()

    while True:
        keywords = list_active_keywords()

        if not keywords:
            logging.info("No active keywords found. Waiting for next scrape interval.")
            await asyncio.sleep(SCRAPE_INTERVAL_SECONDS)
            continue

        logging.info(f"Found {len(keywords)} active keywords.")

        for keyword in keywords:
            logging.info(f"Scraping for keyword: {keyword.value}")

            for source, search_url in NEWS_SOURCES.items():
                logging.info(
                    f"Discovering articles from source='{source}' for keyword='{keyword.value}'"
                )

                try:
                    urls = await discover_articles(search_url, keyword.value)
                    logging.info(
                        f"Discovered {len(urls)} articles from '{source}' for keyword='{keyword.value}'"
                    )

                    for url in urls:
                        if url in seen_urls:
                            continue

                        seen_urls.add(url)

                        try:
                            logging.info(f"Processing article: {url}")
                            process_article(url, keyword.value)
                        except Exception as e:
                            logging.error(
                                f"Error processing article {url}: {e}"
                            )

                        # polite crawling
                        await asyncio.sleep(1)

                except Exception as e:
                    logging.error(
                        f"Error discovering articles from source='{source}': {e}"
                    )

        logging.info(
            f"Scraping loop finished. Sleeping for {SCRAPE_INTERVAL_SECONDS} seconds."
        )
        await asyncio.sleep(SCRAPE_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(run_scraper_loop())
