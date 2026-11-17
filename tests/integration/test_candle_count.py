from playwright.sync_api import Page, expect

from pages.count_page import CountPage
from pages.quiz_page import QuizPage


def test_reaching_target_completes_challenge(page: Page):
    QuizPage(page).open()
    counting = CountPage(page)
    counting.open_counting()

    target = counting.target_number()
    assert 1 <= target <= 8

    expect(counting.counter).to_have_text("0")
    for _ in range(target):
        counting.light_candle()

    expect(counting.counter).to_have_text(str(target))
    expect(counting.light_button).to_be_disabled()
    expect(counting.next_challenge).to_be_visible()

def test_restart_resets_counter_and_keeps_target(page: Page):
    QuizPage(page).open()
    counting = CountPage(page)
    counting.open_counting()

    target = counting.target_number()
    counting.light_candle()
    expect(counting.counter).to_have_text("1")

    counting.restart()

    expect(counting.counter).to_have_text("0")
    expect(counting.target).to_have_text(str(target))
    expect(counting.light_button).to_be_enabled()