import pytest
from playwright.sync_api import Page, expect
from tests.helpers import playwright_login
from tests.factories import PublicRecipeFactory


@pytest.fixture
def public_recipes(db):
    PublicRecipeFactory(name="Veřejný recept", description="Super recept").save()


@pytest.mark.integration
def test_seeing_recipe_from_public_recipe(live_server, page: Page, public_recipes):
    playwright_login(page)
    page.goto("dashboard")

    # Go to index
    page.locator('a:has-text("databáze receptů")').click()

    expect(page).to_have_url("/public-recipe/")
    expect(page.locator("body")).to_contain_text("Veřejný recept")

    # See recipe detail
    page.locator('a:has-text("Veřejný recept")').click()

    expect(page.locator("body")).to_contain_text("návod k přípravě")
    expect(page.locator("body")).to_contain_text("Super recept")

    # TODO: mark as favorite

    # TODO: filter selection
