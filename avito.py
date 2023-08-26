import asyncio
import logging
import os
from typing import List

import pandas as pd
from playwright.async_api import async_playwright

from tg import TelegramBot

logging.basicConfig()
logger = logging.getLogger("Avito")
logger.setLevel(logging.DEBUG)


class AvitoSearch:
    def __init__(self):
        self.bot = TelegramBot()
        self.page = None
        self.browser = None
        self.context = None
        self.search_url = (
            "https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/sdam/magazin"
            "-ASgBAQICAUSwCNRWAUCeww0UiNk5?f"
            "=ASgBAQECAkSwCNRW9BKk2gECQJ7DDRSI2TnIwA4U1uqZAgJFthMVeyJmcm9tIjozMCwid"
            "G8iOm51bGx9xpoMFnsiZnJvbSI6MCwidG8iOjEwMDAwMH0&s=104"
        )

    async def init_browser(self) -> None:
        async with async_playwright() as p:
            logger.info(msg="Init browser")
            self.browser = await p.chromium.launch(headless=True)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            await self.page.goto(self.search_url)
            logger.info(msg="Browser inited")
            while True:
                await self.get_pages()
                url_pages = await self.get_url_pages()
                url_to_tg = self.check_page_is_new(url_pages)
                for url in url_to_tg:
                    await self.bot.send_message(chat_id=os.getenv("CHAT_ID"), msg=url)
                await asyncio.sleep(30)
                logger.info(msg="Updating web page")
                await self.page.reload()

    async def get_pages(self) -> None:
        logger.info(msg="Searching pages")
        text = await self.page.locator(
            ".iva-item-dateInfoStep-_acjp"
        ).all_text_contents()
        good_time = []
        for time in text:
            if time.find("минут") != -1:
                good_time.append(time)
        for time in good_time:
            await self.page.locator(f"text={time}").click()
        logger.info(msg="Pages searched")

    async def get_url_pages(self) -> List[str]:
        logger.info("Get URL of pages")
        pages = self.context.pages[1:]
        for page in pages:
            await page.close()
        return [i.url for i in pages]

    @staticmethod
    def check_page_is_new(url_pages: List[str]) -> List[str]:
        url_to_tg = []
        try:
            df = pd.read_excel("checked_url.xlsx")
        except FileNotFoundError:
            df = pd.DataFrame(columns=["url"])
            df.to_excel("checked_url.xlsx", index=False)
        for url in url_pages:
            if url not in df.url.to_list():
                df.loc[len(df)] = url
                url_to_tg.append(url)
        df.to_excel("checked_url.xlsx", index=False)
        return url_to_tg
