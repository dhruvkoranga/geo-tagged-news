import logging
from typing import Set
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def discover_articles(search_url: str, keyword: str) -> Set[str]:
    logging.info(f"Starting discovery for keyword='{keyword}'")

    links: Set[str] = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # 1. Open search page
            await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)

            # 2. Locate search input
            search_input = await page.wait_for_selector(
                'input[name="search_txt"]',
                timeout=10000
            )

            # 3. Type keyword
            await search_input.fill("")
            await search_input.type(keyword, delay=50)

            # 4. Press Enter
            await search_input.press("Enter")

            # 5. Wait for results container
            await page.wait_for_selector(
                "div.container-fluid.row-content",
                timeout=20000
            )

            logging.info("Search results loaded")

            # 6. Extract article links
            article_elements = await page.query_selector_all(
                "div.container-fluid.row-content blockquote a[href]"
            )

            for el in article_elements:
                href = await el.get_attribute("href")
                if href and href.startswith("https://www.globaltimes.cn/page/"):
                    links.add(href)

            logging.info(f"Discovered {len(links)} articles for keyword='{keyword}'")

        except PlaywrightTimeoutError as e:
            logging.error(f"Timeout while scraping keyword='{keyword}': {e}")

        except Exception as e:
            logging.error(f"Unexpected error while scraping keyword='{keyword}': {e}")

        finally:
            await browser.close()

    return links
