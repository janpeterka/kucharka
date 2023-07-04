import pytest
from playwright.sync_api import Page, expect
from tests.helpers import playwright_login


@pytest.mark.integration
def test_base_pages(live_server, page: Page):
    playwright_login(page)

    expect(page.locator("body")).to_contain_text("vítej!")

    # page.goto("/ingredient/")
    page.locator('a.nav-link.active:has-text("suroviny")').click()
    expect(page.locator("body")).to_contain_text("moje suroviny")

    # page.goto("/recipe/")
    page.locator('a.nav-link.active:has-text("recepty")').click()
    expect(page.locator("body")).to_contain_text("moje recepty")

    # page.goto("/event/")
    page.locator('a.nav-link.active:has-text("akce")').click()
    expect(page.locator("body")).to_contain_text("moje akce")

    page.locator('a.nav-link.active:has-text("databáze receptů")').click()
    expect(page.locator("body")).to_contain_text("pokročilé filtrování")

    page.locator('a.nav-link.active:has-text("tipy a triky")').click()
    expect(page.locator("body")).to_contain_text("tipy a návody")
