from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class PageUrls:
    home_url: str = 'https://app.glob.ge/'
    vin_url: str = 'https://app.glob.ge/cars?get_user_car=&search_vin={****}&start_buy_date=&end_buy_date=&make_id=&model=&year=&search_container=&invoice_phone=&invoice_name='


@dataclass(frozen=True)
class Credentials:
    username: str = os.getenv('EMAIL')
    password: str = os.getenv('PASSWORD')


@dataclass(frozen=True)
class GeneralConfig:
    # define timeouts and retries
    retries: int = 3
    page_load_timeout: int = 20000
    default_timeout: int = 10000
    popup_timeout: int = 5000


@dataclass(frozen=True)
class Locators:
    # locator to sign in website
    username_field_1: str = 'Email'
    username_field_2: str = 'input[type="text"]'
    username_field_3: str = 'input[name="email"]'

    password_field_1: str = 'Password'
    password_field_2: str = 'input[type="password"]'
    password_field_3: str = 'input[name="password"]'
    
    sign_in_button_1: str = 'button span[class*="indicator-label"]'
    sign_in_button_2: str = 'button[type="submit"]'
    sign_in_button_3: str = 'button[class="btn btn-primary"]'  


    # Dealer payment page locators
    dealer_locator: tuple[str, ...] = (
        'a[href*="https://app.glob.ge/users/payments/"]',
        'a[href*="/users/payments/"]',
        'a[href*="/users/"]',
    )

    # Verification locators
    sign_in_verification: tuple[str, ...] = ('ul[class*="nav nav-tabs"]', 'span[class*="menu-title"]', 'span[class*="menu-arrow"]')
   
    dealer_payment_page_verification: tuple[str, ...] = (
        'li[class="nav-item mt-2"] a:has-text("Payments")', 
        'li[class="nav-item mt-2"] a:has-text("Fees")', 
        'li[class="nav-item mt-2"] a:has-text("Cars")'
    )

    # Pop-up locators
    popup_close_button: tuple[str, ...] = (
        'button[id="markAsRead"]',
        'button[class="btn btn-light"]',
        'button[class="modal-footer"]:has-text("Accept")'
    )
    

@dataclass(frozen=True)
class Settings:
    general_settings: GeneralConfig = GeneralConfig()
    credentials: Credentials = Credentials()
    urls: PageUrls = PageUrls()
    locators: Locators = Locators()


