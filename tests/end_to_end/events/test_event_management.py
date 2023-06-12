import pytest
from playwright.sync_api import expect
from tests.helpers import playwright_login, with_authenticated_user
from tests.factories import RecipeFactory, IngredientFactory


@pytest.fixture
def recipes(db, app):
    with_authenticated_user(app, username="user")

    banana = IngredientFactory(name="banana")
    flour = IngredientFactory(name="flour")
    sugar = IngredientFactory(name="sugar")
    butter = IngredientFactory(name="butter")
    cinnamon = IngredientFactory(name="cinnamon")

    recipe = RecipeFactory()
    recipe.add_ingredient(banana, 100)
    recipe.add_ingredient(flour, 100)
    recipe.add_ingredient(sugar, 100)
    recipe.add_ingredient(butter, 100)
    recipe.add_ingredient(cinnamon)

    return recipe


@pytest.mark.integration
def test_event_management(live_server, recipes, page):
    playwright_login(page)

    page.goto("dashboard")

    page.get_by_role("link", name="akce").click()
    page.get_by_role("button", name="akci").click()
    page.get_by_placeholder("např. Tábor 2023").click()
    page.get_by_placeholder("např. Tábor 2023").fill("Testovací akce")
    page.get_by_placeholder("od").fill("2023-09-03")
    page.get_by_placeholder("do").fill("2023-09-12")
    page.get_by_placeholder("základní, u jednotlivých jídel je možné změnit").fill("12")
    page.get_by_placeholder("přidat akci").click()

    expect(page.locator("body")).to_contain_text("Testovací akce")
    expect(page.locator("body")).to_contain_text("od 03.09.2023")
    expect(page.locator("body")).to_contain_text("upravit")

    # TODO: generate


# TODO:
# - test event creation
# - test adding recipes
# - test exports
