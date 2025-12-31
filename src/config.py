import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    RETRIES = 3

    PAGE_LOAD_TIMEOUT = 20000
    DEFAULT_TIMEOUT = 10000

    URL = 'https://app.glob.ge/'
    USERNAME = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')

    # locator element for username and password fields
    USERNAME_FIELD_1 = 'Email'
    USERNAME_FIELD_2 = 'input[type="text"]'
    USERNAME_FIELD_3 = 'input[name="email"]'

    PASSWORD_FIELD_1 = 'Password'
    PASSWORD_FIELD_2 = 'input[type="password"]'
    PASSWORD_FIELD_3 = 'input[name="password"]'

    SIGN_IN_BUTTON_1 = 'button span[class*="indicator-label"]'
    SIGN_IN_BUTTON_2 = 'button[type="submit"]'
    SIGN_IN_BUTTON_3 = 'button[class="btn btn-primary"]'    

    SIGN_IN_VERIFICATION = ['ul[class*="nav nav-tabs"]', 'span[class*="menu-title"]', 'span[class*="menu-arrow"]']

    # VIN_URL = 'https://app.glob.ge/cars?get_user_car=&search_vin={****}&start_buy_date=&end_buy_date=&make_id=&model=&year=&search_container=&invoice_phone=&invoice_name='
