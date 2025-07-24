import asyncio
import re

import clean_links
import db

from db import grab_link
from playwright.async_api import async_playwright, TimeoutError

cleaned_links = []

async def scrape_youtube_links(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Changed wait_until to 'domcontentloaded' and increased timeout
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait for a common YouTube element to be sure the page is loaded
            await page.wait_for_selector("ytd-watch-flexy", timeout=60000)

            # Get all hrefs from anchor tags
            links = await page.eval_on_selector_all(
                "a",
                "elements => elements.map(el => el.href)"
            )

            youtube_links = [
                link for link in links if re.match(r"^https://www\.youtube\.com/watch\?", link)
            ]

            return youtube_links

        except TimeoutError:
            print(f"Timeout while loading {url}")
            return []
        except Exception as e:
            print(f"Error while scraping {url}: {str(e)}")
            return []
        finally:
            await browser.close()


async def main():
    while True:
        try:
            video_id = grab_link()
            url = "https://www.youtube.com/watch?v=" + video_id
            links = await scrape_youtube_links(url)
            for x in links:
                clean_link = clean_links.extract_youtube_id(x)
                cleaned_links.append(clean_link)
            final_links = list(set(cleaned_links))
            amount_of_links = len(final_links)
            for x in final_links:
                print(x)
            db.save_link(final_links, amount_of_links)
            cleaned_links.clear()
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())