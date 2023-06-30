import pytest
from playwright.sync_api import Page, expect
from tests.helpers import playwright_login


@pytest.mark.integration
def test_ingredient_creation(live_server, page: Page):
    playwright_login(page, "user")

    page.get_by_role("link", name="suroviny").click()
    page.get_by_role("link", name="přidat surovinu").click()

    # Create ingredient
    page.get_by_placeholder("název suroviny").click()
    page.get_by_placeholder("název suroviny").fill("Bam")
    page.get_by_placeholder("název suroviny").press("Tab")
    page.get_by_placeholder("přidat surovinu").press("Enter")

    expect(page.locator("body")).to_contain_text("Bam")

    # Edit ingredient
    page.get_by_role("link", name="upravit").click()
    page.get_by_role("combobox", name="počítané v").select_option("2")
    page.get_by_placeholder("název suroviny").click()
    page.get_by_placeholder("název suroviny").fill("Brambora")
    page.get_by_role("combobox", name="kategorie").select_option("3")
    page.get_by_role("button", name="uložit změnu").click()

    expect(page.locator("body")).to_contain_text("Brambora")
    expect(page.locator("body")).to_contain_text("kusy")
