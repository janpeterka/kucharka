from unidecode import unidecode

from flask_security import login_required, current_user

from app.helpers.helper_flask_view import HelperFlaskView


class UserStatisticsView(HelperFlaskView):
    decorators = [login_required]

    def before_request(self, name, *args, **kwargs):
        self.user = current_user
        self.validate_operation(id, self.user)

    def draft_recipes(self):
        return self.template(template_name="recipes/_draft_recipes.html.j2")

    def ingredients_without_category(self):
        ingredients = [i for i in self.user.personal_ingredients if i.without_category]

        return self.template(
            template_name="ingredients/_ingredients_without_category.html.j2",
            ingredients=ingredients,
        )

    def ingredients_without_measurement(self):
        ingredients = [
            i for i in self.user.personal_ingredients if i.without_measurement
        ]

        return self.template(
            template_name="ingredients/_ingredients_without_measurement.html.j2",
            ingredients=ingredients,
        )

    def recipes_without_category(self):
        recipes = [i for i in self.user.recipes if i.without_category]

        return self.template(
            template_name="recipes/_recipes_without_category.html.j2", recipes=recipes
        )

    def events(self):
        return self.template(template_name="events/_list.html.j2")

    def recipes(self):
        self.recipes = sorted(
            self.user.visible_recipes, key=lambda x: unidecode(x.name.lower())
        )
        return self.template(template_name="recipes/_recipe_list.html.j2")

    def ingredients(self):
        self.ingredients = sorted(
            self.user.personal_ingredients, key=lambda x: unidecode(x.name.lower())
        )
        return self.template(template_name="ingredients/_list.html.j2")
