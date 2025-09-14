import re
from playwright.sync_api import expect
from pages.base_page import BasePage

class LivePage(BasePage):

    @property
    def sport_header(self):
        return self.locator("span.breadcrumb-title")

    @property
    def event_rows(self):
        return self.page.locator("ms-grid ms-event")
    
    @property
    def active_tab(self):
        return self.page.locator("vn-menu-item.active.menu-item").first
    
    def is_tab_active(self, tab_name: str) -> bool:
        locator = self.page.locator("vn-menu-item.active.menu-item", has_text=tab_name)
        return locator.count() > 0

    def wait_until_ready(self, timeout: int = 8000) -> None:
        expect(self.page).to_have_url(re.compile(r"/sports/tennis-5"), timeout=timeout)
        
        expect(self.sport_header).to_have_text("Tennis Betting", timeout=timeout)

    def open_event_by_index(self, index: int = 0, skip_suspended: bool = True, timeout: int = 8000) -> None:
        expect(self.event_rows.first).to_be_visible(timeout=timeout)
        rows = self.event_rows
        count = rows.count()

        valid_rows = []
        for i in range(count):
            row = rows.nth(i)
            if skip_suspended:
                if row.get_by_text("Suspended", exact=False).count() > 0:
                    continue
                if row.get_by_text("Finished", exact=False).count() > 0:
                    continue
                if row.locator("[class*='suspend']").count() > 0:
                    continue
            valid_rows.append(row)

        link = valid_rows[index].locator("a.grid-info-wrapper, a[href*='/sports/events/']").first
        self.click(link)
        expect(self.page).to_have_url(re.compile(r"/sports/events/"), timeout=timeout)