import pytest
from playwright.sync_api import Page, expect
from tests.helpers import playwright_login


@pytest.mark.integration
def test_unlogged(live_server, page: Page):
    page.goto("dashboard")
    expect(page.locator("body")).to_contain_text("přihlášení")


@pytest.mark.integration
def test_base_pages(db, live_server, page: Page):
    playwright_login(page)

    import time

    page.goto("/")
    expect(page.locator("body")).to_contain_text("vítej!")

    page.goto("/event/")
    # expect(page.locator("body")).to_contain_text("událost")
    # expect(page.locator("body")).to_contain_text("opakovaná událost")
    # expect(page.locator("body")).to_contain_text("minulé události")
