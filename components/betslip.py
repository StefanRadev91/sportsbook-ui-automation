from playwright.sync_api import expect
from pages.base_page import BasePage

class BetSlip(BasePage):

    @property
    def tab(self):
        return self.page.locator("li[role='tab'] >> text=Bet Slip")

    @property
    def badge(self):
        return self.tab.locator("ds-notification-bubble").first

    @property
    def container(self):
        return self.page.locator("div").filter(has_text="Selections").first

    @property
    def mobile_badge(self):
        return self.page.locator(
            "bs-quick-bet-header .quick-bet-counter, span.quick-bet-counter"
        ).first

    @property
    def mobile_container(self):
        return self.page.locator(".quick-bet-container, .betslip-digital")

    def open(self):
        if self.tab.count() > 0 and self.tab.is_visible():
            self.click(self.tab)

    def has_pick(self, selection_name: str) -> bool:
        if self.container.count() > 0:
            return (
                self.container.get_by_text(selection_name, exact=False).count() > 0
            )
        return (
            self.mobile_container.get_by_text(selection_name, exact=False).count() > 0
        )

    def has_any_selection(self) -> bool:
        if self.container.count() > 0:
            return self.container.get_by_text("Selections", exact=False).count() > 0
        return (
            self.mobile_container.locator(":text('Quick Bet')").count() > 0
            or self.mobile_container.count() > 0
        )

    def wait_until_badge_count(self, expected: int, timeout: int = 8000):
        mobile_header = self.page.locator("bs-quick-bet-header").first
        mobile_counter = self.mobile_badge
        if mobile_header.count() > 0:
            
            try:
                expect(mobile_header).to_be_visible(timeout=timeout)
                expect(mobile_counter).to_have_text(str(expected), timeout=timeout)
                return
            except Exception:
                pass

        try:
            expect(mobile_counter).to_have_text(
                str(expected), timeout=int(timeout * 0.7)
            )
            return
        except Exception:
            pass

        expect(self.badge).to_have_text(str(expected), timeout=timeout)