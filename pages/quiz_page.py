from playwright.sync_api import Page



class QuizPage:
    def __init__(self, page:Page): self.page = page
    def open(self):
        return self.page.goto("https://chayamm-lab.github.io/english-for-kids/")