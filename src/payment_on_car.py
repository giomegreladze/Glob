from playwright.async_api import Error, TimeoutError

import logging
import asyncio

from src.config import Settings


class Payments:
    def __init__(self, page, settings: type[Settings] = Settings) -> None:
        self.page = page
        self.settings = settings
        self.urls = settings.urls
        self.credentials = settings.credentials
        self.locators = settings.locators
        self.config = settings.general_settings

    
    async def navigate_to_payments_page(self, vin: str) -> bool:
        """Navigate to Dealer Payments page after filtering by VIN."""
        vin_found = await self.find_vin(vin)
        if not vin_found:
            return False
        else:
            return await self.navigate_to_dealer_payments()


    async def find_vin(self, vin: str) -> bool:
        """Filter website by VIN."""
        for i in range(self.config.retries):
            logging.info(f'-- Finding VIN attempt {i+1}/{self.config.retries}')
            vin_url = self.urls.vin_url.replace('{****}', vin)
            try:
                await self.page.goto(vin_url, wait_until='domcontentloaded', timeout=self.config.page_load_timeout)
                return True
            except Error:
                logging.error(f'Page did not load in {self.config.page_load_timeout} ms for VIN: {vin}. Retrying')
        return False
        

    async def navigate_to_dealer_payments(self) -> bool:
        """Navigate to Dealer Payments page after filtering by VIN."""
        dealer_locators = [self.page.locator(locator) for locator in self.locators.dealer_locator]

        dealer_url = ''
        for locator in dealer_locators:
            try:
                await locator.wait_for(state='visible', timeout=self.config.default_timeout)
                dealer_url = await locator.get_attribute('href')
                break
            except TimeoutError:
                logging.warning(f'-- Error finding Dealer locator {locator}. Retrying...')
            except Error:
                logging.warning(f'-- Error getting href attribute from locator {locator}. Retrying...')

        if dealer_url:
            await self.page.goto(dealer_url)
            verification = await self.verify_dealer_payments_page()
            if verification:
                logging.info('-- Successfully navigated to Dealer Payments page.')
                return True
            else:
                logging.error('-- Dealer Payments page verification failed after navigation.')
                return False
        else:
            logging.error('-- Could not find Dealer URL from any of the locators provided.')
            return False
        


    async def verify_dealer_payments_page(self) -> bool:
        """Verify that we are on the Dealer Payments page."""
        for locator in self.locators.dealer_payment_page_verification:
            try:
                await self.page.wait_for_selector(locator, state='visible', timeout=self.config.default_timeout)
                await asyncio.sleep(3)
                return True
            except TimeoutError:
                logging.error(f'-- Dealer Payments page verification failed on locator {locator}. Retrying...')
        return False

            

        