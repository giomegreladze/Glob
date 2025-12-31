import logging
import asyncio

from playwright.async_api import async_playwright

from src.browser_manager import BrowserManager
from src.auth import SignIn
from src.payment_on_car import Payments


logging.basicConfig(
    level=logging.INFO,
    # filename='glob.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)


async def main():
    async with BrowserManager(headless=False) as page:

        if not await SignIn(page).auth():
            return None
        await Payments(page).navigate_to_payments_page('JTMAB3FV5RD215740')

asyncio.run(main())