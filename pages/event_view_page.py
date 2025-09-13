from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re

class EventViewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.last_odds: float | None = None

    @property
    def match_winner_market(self):
        return self.page.get_by_text("Match Winner", exact=False).first

    @property
    def first_selection(self):
        return self.page.locator("ms-option .option-pick").first

    @property
    def first_selection_odds(self):
        return self.first_selection.locator("div.value.option-value").first

    @property
    def first_selection_indicator(self):
        return self.first_selection.locator(".option-indicator").first

    def wait_until_loaded(self, timeout: int = 8000):
        self.page.wait_for_url("**/sports/events/*", timeout=timeout)
        expect(self.match_winner_market).to_be_visible(timeout=timeout)
        expect(self.first_selection).to_be_visible(timeout=timeout)
        expect(self.first_selection_odds).to_be_visible(timeout=timeout)

    def pick_first(self):
        self.click(self.first_selection.locator(".option-indicator"))

    def wait_until_first_selection_highlighted(self, timeout: int = 5000) -> bool:
        indicator = self.first_selection.locator(".option-indicator")
        expect(indicator).to_have_class(re.compile(".*selected.*"), timeout=timeout)
        return True

    def _odds_text(self) -> str:
        txt = self.first_selection_odds.inner_text().strip()
        return re.sub(r"\s+", " ", txt)

    def _odds_value(self, text: str | None = None) -> float | None:
        t = text if text is not None else self._odds_text()
        m = re.search(r"(\d+(?:\.\d+)?)", t)
        return float(m.group(1)) if m else None

    def _indicator_dir(self) -> str | None:
        cls = (self.first_selection_indicator.get_attribute("class") or "").lower()
        if "increased" in cls:
            return "up"
        if "decreased" in cls:
            return "down"
        return None

    def wait_for_match_winner_odds_update(self, timeout: int = 60_000) -> dict:
        old_text = self._odds_text()
        old_val = self._odds_value(old_text)

        self.wait_for_text_change(self.first_selection_odds, old_text, timeout=timeout)

        new_text = self._odds_text()
        new_val = self._odds_value(new_text)
        direction = self._indicator_dir()                 
        self.last_odds = new_val

        return {
            "old_text": old_text,
            "new_text": new_text,
            "old_value": old_val,
            "new_value": new_val,
            "direction": direction,
        }