import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

VIEWPORT_SIZES = [
    {"width": 1920, "height": 1080},
    {"width": 1366, "height": 768},
    {"width": 1440, "height": 900},
]

async def main():
    target_handle = "zawyacinema"
    target_url = f"https://www.instagram.com/{target_handle}/"

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--no-blink-features=AutomationControlled',
                '--disable-blink-features=AutomationControlled',
            ]
        )
        
        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport=random.choice(VIEWPORT_SIZES),
            locale='en-US',
        )

        page = await context.new_page()
        
        # Go to Instagram
        await page.goto(target_url, timeout=60000, wait_until='domcontentloaded')
        
        # Wait for the network to be mostly idle, a good sign the page is settling.
        print("Page navigation complete. Waiting for network to be idle...")
        await page.wait_for_load_state('networkidle', timeout=10000)
        
        
        post_selector = f'a[href^="/{target_handle}/p/"]'

        try:
            print("Waiting for post links to be visible...")
            await page.locator(post_selector).first.wait_for(timeout=10000)
            print("Post links are visible!")
            post_locators = await page.locator(post_selector).all()
            print(f'Found {len(post_locators)} matching post links:')
            for i, locator in enumerate(post_locators):
                href = await locator.get_attribute('href')
                print(f"{i+1}: {href}")
            await browser.close()
            return

        except Exception as e:
            print(f"Failed to find posts: {e}")
            await page.screenshot(path="page_loading_failed.png")
            print("Screenshot saved to page_loading_failed.png")
        finally:
            print("Closing browser.")
            await browser.close()

asyncio.run(main())
