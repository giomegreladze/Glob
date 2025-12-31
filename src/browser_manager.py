from playwright.async_api import async_playwright

class BrowserManager:
    def __init__(self, headless=False):
        self.headless=headless

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless, slow_mo=3000)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        return self.page
    
    async def __aexit__(self, *args):
        await self.browser.close()
        await self.playwright.stop()
