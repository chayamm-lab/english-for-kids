from playwright.sync_api import Page


class CountPage:
    def __init__(self, page: Page):
        self.page = page
        self.target = page.locator("#tNum")
        self.counter = page.locator("#cNum")
        self.light_button = page.get_by_role("button", name="הדליקו נר", exact=True)
        self.next_challenge = page.get_by_role("button", name="עוד אתגר", exact=True)

    def open_counting(self):
        self.page.get_by_role("button", name="סופרים נרות Count", exact=True).click()

    def target_number(self):
        return int(self.target.inner_text())

    def light_candle(self):
        self.light_button.click()

    def restart(self):
        self.page.get_by_role(
            "button", name="מתחילים מחדש", exact=True
        ).click()