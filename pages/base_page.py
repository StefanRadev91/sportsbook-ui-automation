from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def by_text(self, text: str, exact: bool = False):
        return self.page.get_by_text(text, exact=exact)

    def by_role(self, role: str, name: str = None):
        return self.page.get_by_role(role=role, name=name)

    def by_placeholder(self, text: str):
        return self.page.get_by_placeholder(text)

    def by_label(self, text: str):
        return self.page.get_by_label(text)

    def by_title(self, text: str):
        return self.page.get_by_title(text)

    def locator(self, selector: str):
        return self.page.locator(selector)

    def click(self, locator):
        self.element_to_be_visible(locator)
        locator.click()

    def fill(self, locator, value: str):
        self.element_to_be_visible(locator)
        locator.fill(value)

    def select_option(self, locator, value=None, label=None, index=None):
        self.element_to_be_visible(locator)
        locator.select_option(value=value, label=label, index=index)

    def element_to_be_visible(self, locator):
        expect(locator).to_be_visible()

    def get_text(self, locator) -> str:
        self.element_to_be_visible(locator)
        return locator.inner_text()

    def is_visible(self, locator) -> bool:
        return locator.is_visible()

    def has_class(self, locator, class_name: str) -> bool:
        classes = locator.get_attribute("class") or ""
        return class_name in classes

    def wait_for_text_change(self, locator, old_value: str, timeout: int = 10000):
        expect(locator).not_to_have_text(old_value, timeout=timeout)