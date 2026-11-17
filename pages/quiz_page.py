from playwright.sync_api import Page



class QuizPage:

    def __init__(self, page:Page): self.page = page

    def open(self):
        return self.page.goto("https://chayamm-lab.github.io/english-for-kids/")

    def open_listening(self):
        self.page.get_by_role("button", name="מקשיבים ובוחרים Listen").click()

    def current_word_id(self):
        return self.page.locator("#listenPlay").get_attribute("data-word-id")

    def choose_picture(self, name: str):
        self.page.locator("#lOpts").get_by_role(
            "button", name=name, exact=True
        ).click()

    def wrong_picture(self, correct_name: str):
        for button in self.page.locator("#lOpts").get_by_role("button").all():
            if button.get_attribute("aria-label") != correct_name:
                return button

        raise AssertionError("לא נמצאה תמונה שגויה לבחירה")

    def replay_word(self):
        self.page.locator("#hearBtn").click()