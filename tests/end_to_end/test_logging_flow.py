import pytest
from playwright.sync_api import Page, expect
from tests.helpers import playwright_login


@pytest.mark.integration
def test_logging_in(live_server, page: Page):
    page.goto("dashboard")

    expect(page.locator("body")).to_contain_text("přihlášení")

    playwright_login(page)

    expect(page.locator("body")).to_contain_text("vítej!")
