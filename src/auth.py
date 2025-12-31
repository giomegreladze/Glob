import logging
from playwright.async_api import Page, TimeoutError, Error
from src.config import Config

class SignIn:
    def __init__(self, page: Page, config: type[Config] = Config) -> None:
        self.page = page
        self.config = config


    async def auth(self) -> bool:
        for i in range(self.config.RETRIES):
            logging.info(f'-- Sign in attempt {i+1}/{self.config.RETRIES}')
            try:
                await self.page.goto(self.config.URL, wait_until='domcontentloaded', timeout=self.config.PAGE_LOAD_TIMEOUT)
                logging.info(f'-- Navigated to {self.config.URL} successfully.')

                if not await self._fill_email(self.config.USERNAME):
                    continue
                if not await self._fill_password(self.config.PASSWORD):
                    continue
                if not await self._click_sign_in():
                    continue
                if await self._is_authenticated():
                    logging.info('-- Sign in Successful')
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
                await locator.wait_for(state='visible', timeout=self.config.DEFAULT_TIMEOUT)
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
            self.page.get_by_placeholder(self.config.USERNAME_FIELD_1),
            self.page.locator(self.config.USERNAME_FIELD_2),
            self.page.locator(self.config.USERNAME_FIELD_3),
        ]
        return await self._fill_fields(email_locators, email, "Email")


    async def _fill_password(self, password: str) -> bool:
        password_locators = [
            self.page.get_by_placeholder(self.config.PASSWORD_FIELD_1),
            self.page.locator(self.config.PASSWORD_FIELD_2),
            self.page.locator(self.config.PASSWORD_FIELD_3),
        ]

        return await self._fill_fields(password_locators, password, "Password")


    async def _click_sign_in(self) -> bool:
        sign_in_locator = [
            self.page.locator(self.config.SIGN_IN_BUTTON_1),
            self.page.locator(self.config.SIGN_IN_BUTTON_2),
            self.page.locator(self.config.SIGN_IN_BUTTON_3),
        ]
        for locator in sign_in_locator:
            try:
                await locator.wait_for(state='visible', timeout=self.config.DEFAULT_TIMEOUT)
                await locator.click()
                logging.info('-- Sign in button clicked successfully.')
                return True
            except TimeoutError:
                logging.warning(f'-- Error finding sign in button {locator}. Retrying...')
            except Error:
                logging.warning(f'-- Error clicking sign in button {locator}. Retrying...')
        logging.error('-- Sign in button not found.')
        return False
    

    async def _is_authenticated(self) -> bool:
        for locator in self.config.SIGN_IN_VERIFICATION:
            try:
                await self.page.wait_for_selector(locator, timeout=self.config.PAGE_LOAD_TIMEOUT)
                return True
            except TimeoutError:
                logging.warning(f'-- Verification locator "{locator}" not found. Trying next...')
        logging.error('-- Authentication verification failed.')
        return False