import asyncio
from playwright.async_api import async_playwright

urls = [
    "https://help.fundednext.com/en/collections/13565526-general-faq",
    "https://help.fundednext.com/en/collections/13567126-eligibility-verification",
    # add all your URLs here...
]

keywords = ["coupon", "promo", "discount", "%off", "% off", "code", "voucher", "offer"]

async def run():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context()

        for url in urls:
            try:
                page = await context.new_page()
                await page.goto(url, wait_until="networkidle")

                content = await page.content()
                text = await page.inner_text("body")

                found = [kw for kw in keywords if kw in text.lower()]
                if found:
                    print(f"🔎 Potential promo mention found on {url}")
                    print(f"   ➝ Found keywords: {set(found)}")
                    print("--------------------------------------------------")

                await page.close()
            except Exception as e:
                print(f"⚠️ Error loading {url}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
