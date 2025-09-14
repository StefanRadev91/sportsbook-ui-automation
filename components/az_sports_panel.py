from playwright.sync_api import expect
from pages.base_page import BasePage
import re

class AZSportsPanel(BasePage):

    @property
    def cookies_banner(self):
        return self.locator("#onetrust-policy-title")

    @property
    def cookies_accept(self):
        return self.page.locator("#onetrust-accept-btn-handler")
    
    @property
    def az_tab(self):
        return self.by_role("link", "A-Z Sports")

    @property
    def panel(self):
        return self.locator("div,section").filter(has_text="A-Z").first

    def sport_item(self, sport_name: str):
        return self.panel.get_by_text(sport_name, exact=False)

    @property
    def hamburger(self):
        return self.page.locator("i.theme-az-menu-search")

    @property
    def tennis_tile(self):
        return self.page.get_by_text("Tennis", exact=True).first

    def open(self):
        self.click(self.az_tab)
        expect(self.panel).to_be_visible(timeout=3000)

    def select_sport(self, sport_name: str, sport_slug: str | None = None, timeout: int = 10000):
        item = self.sport_item(sport_name)
        expect(item).to_be_visible(timeout=3000)
        self.click(item)
        if sport_slug:
            expect(self.page).to_have_url(re.compile(fr"/sports/{re.escape(sport_slug)}"), timeout=timeout)

    def go_to_tennis(self, timeout: int = 10000):
        try:
            self.cookies_accept.wait_for(state="visible", timeout=3000)
            if self.cookies_accept.is_visible():
                self.click(self.cookies_accept)
        except Exception:
            pass

        if self.hamburger.is_visible():
            self.click(self.hamburger)
            self.click(self.tennis_tile)
        else:
            self.open()
            self.select_sport("Tennis", sport_slug="tennis-5", timeout=timeout)