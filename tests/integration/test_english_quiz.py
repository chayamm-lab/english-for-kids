from playwright.sync_api import Page
from pages.quiz_page import QuizPage

def test_quiz_page_loads(page:Page):
    response = QuizPage(page).open()
    assert response is not None
    assert response.ok