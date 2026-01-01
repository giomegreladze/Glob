import logging
from playwright.async_api import Page, TimeoutError, Error
from src.config import Settings


class SignIn:
    def __init__(self, page: Page, settings: type[Settings] = Settings) -> None:
        self.page = page
        self.settings = settings
        self.urls = settings.urls
        self.credentials = settings.credentials
        self.locators = settings.locators
        self.config = settings.general_settings


    async def auth(self) -> bool:
        for i in range(self.config.retries):
            logging.info(f'-- Sign in attempt {i+1}/{self.config.retries}')
            try:
                await self.page.goto(self.urls.home_url, wait_until='domcontentloaded', timeout=self.config.page_load_timeout)
                logging.info(f'-- Navigated to {self.urls.home_url} successfully.')

                if not await self._fill_email(self.credentials.username):
                    continue
                if not await self._fill_password(self.credentials.password):
                    continue
                if not await self._click_sign_in():
                    continue
                if await self._is_authenticated():
                    logging.info('-- Sign in Successful')
                    await self._close_popups()
                    return True
            except TimeoutError:
                logging.error(f'-- Sign in attempt {i+1} failed. Retrying...')
            except Error:
                logging.error(f'-- Unexpected error during sign in attempt {i+1}. Retrying...')
        logging.error('-- All sign in attempts failed.')
        return False

    
    async def _fill_fields(self, locators: list, value: str, field_name: str) -> bool:
        for locator in locators:
            try:
                await locator.wait_for(state='visible', timeout=self.config.default_timeout)
                await locator.fill(value)
                logging.info(f'-- {field_name} filled successfully.')
                return True
            except TimeoutError:
                logging.warning(f'-- Error finding {field_name} field {locator}. Retrying...')
            except Error:
                logging.warning(f'-- Error filling {field_name} field {locator}. Retrying...')
        logging.error(f'-- {field_name} field not found.')
        return False
    

    async def _fill_email(self, email: str) -> bool:
        email_locators = [
            self.page.get_by_placeholder(self.locators.username_field_1),
            self.page.locator(self.locators.username_field_2),
            self.page.locator(self.locators.username_field_3),
        ]
        return await self._fill_fields(email_locators, email, "Email")


    async def _fill_password(self, password: str) -> bool:
        password_locators = [
            self.page.get_by_placeholder(self.locators.password_field_1),
            self.page.locator(self.locators.password_field_2),
            self.page.locator(self.locators.password_field_3),
        ]

        return await self._fill_fields(password_locators, password, "Password")


    async def _click_sign_in(self) -> bool:
        sign_in_locator = [
            self.page.locator(self.locators.sign_in_button_1),
            self.page.locator(self.locators.sign_in_button_2),
            self.page.locator(self.locators.sign_in_button_3),
        ]
        for locator in sign_in_locator:
            try:
                await locator.wait_for(state='visible', timeout=self.config.default_timeout)
                await locator.click()
                logging.info('-- Sign in button clicked successfully.')
                return True
            except TimeoutError:
                logging.warning(f'-- Error finding sign in button {locator}. Retrying...')
            except Error:
                logging.warning(f'-- Error clicking sign in button {locator}. Retrying...')
        logging.error('-- Sign in button not found.')
        return False
    

    async def _close_popups(self) -> None:
        """Close any pop-ups that may appear after sign-in."""
        for locator in self.locators.popup_close_button:
            try:
                await self.page.wait_for_selector(locator, timeout=self.config.popup_timeout)
                await self.page.locator(locator).click()
                logging.info(f'-- Closed pop-up with locator: {locator}')
                return None
            except TimeoutError:
                continue
        logging.info('-- No pop-ups to close.')
        return None
    

    async def _is_authenticated(self) -> bool:
        for locator in self.locators.sign_in_verification:
            try:
                await self.page.wait_for_selector(locator, timeout=self.config.page_load_timeout)
                return True
            except TimeoutError:
                logging.warning(f'-- Verification locator "{locator}" not found. Trying next...')
        logging.error('-- Authentication verification failed.')
        return False