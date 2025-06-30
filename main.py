import time
import random
import db
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from db import grab_link


def get_sidebar_links(page):
    try:
        page.wait_for_selector("ytd-compact-video-renderer", timeout=5000)
        links = page.eval_on_selector_all(
            "ytd-compact-video-renderer a#thumbnail",
            "elements => elements.map(el => el.href)",
        )
        return links
    except PlaywrightTimeoutError:
        print("Timeout waiting for sidebar links.")
        return []

def collect_random_youtube_links(start_url, max_iterations=25, time_delay=0.5):
    urls = set()
    current_url = start_url
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        for i in range(max_iterations):
            print(f"({i + 1}/{max_iterations}) Collecting links from {current_url}...")
            try:
                page.goto(current_url, timeout=10000)
                new_links = get_sidebar_links(page)
                print(f" Found {len(new_links)} links.")

                for link in new_links:
                    if link and link.startswith("https://www.youtube.com/watch"):
                        urls.add(link)
                if urls:
                    current_url = random.choice(list(urls))
                else:
                    print("No valid links found. Stopping...")
                    break
                time.sleep(time_delay)
            except Exception as e:
                print(f"Error occurred: {e}")
                break
        browser.close()
    return list(urls)

if __name__ == "__main__":
    while True:
        start_url = grab_link()
        collected_urls = collect_random_youtube_links(start_url)
        amount_of_links = len(collected_urls)
        db.save_link(collected_urls, amount_of_links)


    # print("\nCollected URLs: ")
    #for url in collected_urls:
        #print(url)

    # links = []
    # link = grab_link()
    # while len(links) < 10:
        # new_link = os.system("yt-dlp -g " + link)
        # links.append(new_link)
    # for link in links
        # send_command(link)
    # link = grab_link()
    # send_command(link)




