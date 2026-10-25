import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import json
import base64

async def open_website(browser,url):
        page = await browser.new_page()

        try:    

            resources = []
            
            page.on("request",lambda request: resources.append(request.url))
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            html = await page.content()
            screenshot_bytes= await page.screenshot()
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")


            data = {
                    "html": html,
                    "resources": resources,
                    "screenshot": screenshot_base64
                }

            return data, screenshot_bytes

        finally:
            await page.close()

def save_data(data, screenshot_bytes, output_folder):
    output_folder.mkdir(parents=True, exist_ok=True)

    with open(output_folder / "browse.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    (output_folder / "screenshot.png").write_bytes(screenshot_bytes)

def read_urls(file_path):
    urls = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            url = line.strip()

            if url:
                urls.append(url)

    return urls

async def process_urls(file_path):
    urls = read_urls(file_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel="chrome",
            headless=False
        )
        try:
            for index, url in enumerate(urls, start=1):
                output_folder = Path("output") / f"url_{index}"
                data, screenshot_bytes = await open_website(browser,url)

                save_data(data, screenshot_bytes, output_folder)
        finally:
            await browser.close()

asyncio.run(process_urls("input/urls.input"))

    