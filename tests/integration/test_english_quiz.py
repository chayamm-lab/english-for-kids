import pytest
import re
from playwright.sync_api import Page, expect
from pages.quiz_page import QuizPage

PICTURE_NAMES = {
    "menorah": "חנוכייה",
    "candle": "נר",
    "dreidel": "סביבון",
    "donut": "סופגנייה",
    "coin": "מטבע",
    "oil": "שמן",
    "pancake": "לביבה",
    "gift": "מתנה",
    "star": "מגן דוד",
    "flame": "להבה",
}

def test_quiz_page_loads(page:Page):
    response = QuizPage(page).open()
    assert response is not None
    assert response.ok

def test_listening_round_has_word_id(page: Page):
    quiz = QuizPage(page)
    quiz.open()
    quiz.open_listening()

    assert quiz.current_word_id(), "לא נמצא מזהה מילה בסבב ההאזנה"

def test_correct_picture_shows_success(page: Page):
    quiz = QuizPage(page)
    quiz.open()
    quiz.open_listening()

    word_id = quiz.current_word_id()
    assert word_id in PICTURE_NAMES, f"מזהה מילה לא מוכר: {word_id}"

    quiz.choose_picture(PICTURE_NAMES[word_id])

    expect(page.locator("#lFb")).to_have_class(re.compile(r"\bgood\b"))

def test_wrong_picture_shows_retry(page: Page):
    quiz = QuizPage(page)
    quiz.open()
    quiz.open_listening()

    correct_name = PICTURE_NAMES[quiz.current_word_id()]
    wrong_button = quiz.wrong_picture(correct_name)
    wrong_button.click()

    expect(page.locator("#lFb")).to_have_text("נסו שוב")
    expect(wrong_button).to_be_disabled()

def test_correct_picture_after_wrong_choice(page: Page):
    quiz = QuizPage(page)
    quiz.open()
    quiz.open_listening()

    correct_name = PICTURE_NAMES[quiz.current_word_id()]
    feedback = page.locator("#lFb")

    quiz.wrong_picture(correct_name).click()
    expect(feedback).to_have_text("נסו שוב")

    quiz.choose_picture(correct_name)
    expect(feedback).to_have_class(re.compile(r"\bgood\b"))

def test_correct_answer_starts_next_round(page: Page):
    quiz = QuizPage(page)
    quiz.open()
    quiz.open_listening()

    first_word_id = quiz.current_word_id()
    quiz.choose_picture(PICTURE_NAMES[first_word_id])

    expect(page.locator("#listenPlay")).not_to_have_attribute(
        "data-word-id", first_word_id
    )
    expect(page.locator("#lFb")).to_have_text("")

@pytest.mark.parametrize(
    "make_mistake, expected_stars",
    [(False, 1), (True, 0)],
    ids=["first-try", "after-mistake"],
)
def test_listening_score(page: Page, make_mistake: bool, expected_stars: int):
    quiz = QuizPage(page)
    quiz.open()
    quiz.open_listening()

    first_word_id = quiz.current_word_id()
    correct_name = PICTURE_NAMES[first_word_id]

    if make_mistake:
        quiz.wrong_picture(correct_name).click()

    quiz.choose_picture(correct_name)

    expect(page.locator("#listenPlay")).not_to_have_attribute(
        "data-word-id", first_word_id
    )
    expect(page.locator("#lStars .st.on")).to_have_count(expected_stars)

def test_listening_shows_final_score(page: Page):
    quiz = QuizPage(page)
    quiz.open()
    quiz.open_listening()

    for round_number in range(1, 9):
        word_id = quiz.current_word_id()
        correct_name = PICTURE_NAMES[word_id]

        if round_number <= 2:
            quiz.wrong_picture(correct_name).click()

        quiz.choose_picture(correct_name)

        if round_number < 8:
            expect(page.locator("#listenPlay")).not_to_have_attribute(
                "data-word-id", word_id
            )

    expect(
        page.get_by_text("קיבלתם 6 כוכבים מתוך 8", exact=True)
    ).to_be_visible()