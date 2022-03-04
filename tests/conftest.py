import pytest

import datetime

from app import create_app
from app import db as _db


@pytest.fixture
def app(scope="session"):
    app = create_app(config_name="testing")

    @app.context_processor
    def inject_globals():
        from app.data import template_data

        return dict(texts=template_data.texts)

    @app.context_processor
    def utility_processor():
        def human_format_date(date, with_weekday=True, with_relative=True):
            formatted_date = date.strftime("%d.%m.%Y")

            from app.helpers.formaters import week_day

            if with_weekday:
                formatted_date += f" ({week_day(date)})"

            if with_relative:
                if date == datetime.date.today():
                    formatted_date += " - Dnes"
                    # return "Dnes"
                elif date == datetime.date.today() + datetime.timedelta(days=-1):
                    formatted_date += " - Včera"
                    # return "Včera"
                elif date == datetime.date.today() + datetime.timedelta(days=1):
                    formatted_date += " - Zítra"
                    # return "Zítra"
                # else:
                # return date.strftime("%d.%m.%Y")

            return formatted_date

        def link_to(obj, link_type="show"):
            try:
                if link_type == "show":
                    return obj.link_to
                elif link_type == "edit":
                    return obj.link_to_edit

            except Exception:
                raise NotImplementedError(
                    f"This object link_to (with {link_type}) is probably not implemented"
                )

        def formatted_amount(amount):
            import math

            if amount == 0:
                return 0

            if math.floor(amount) == 0:
                digits = 0
            else:
                digits = int(math.log10(math.floor(amount))) + 1

            if digits in [0, 1]:
                # if number is in ones, return with one decimal
                formatted_amount = round(amount, 1)
                # if first decimal is zero
                if int(formatted_amount) == formatted_amount:
                    return int(formatted_amount)
                else:
                    return formatted_amount
            elif digits in (2, 3):
                # if number is in tens or hundereds, return without decimals
                return round(amount)

            return int(amount)

        return dict(
            human_format_date=human_format_date,
            link_to=link_to,
            formatted_amount=formatted_amount,
        )

    return app


@pytest.fixture
def db(app):
    # insert default data
    # with app.app_context():
    #     _db.create_all()

    # db_fill()

    return _db


# def db_fill():
#     # from flask_security import create_user, create_role
#     from app import security

#     roles = [
#         security.datastore.create_role(
#             name="admin",
#             permissions="manage-application,manage-users,login-as,see-debug,see-other,edit-other",
#         ),
#         security.datastore.create_role(
#             name="application_manager",
#             permissions="manage-application,see-other,edit-other",
#         ),
#     ]

#     for role in roles:
#         role.save()

#     users = [
#         security.datastore.create_user(
#             username="user", email="user@sk.cz", password="pass123"
#         ),
#         security.datastore.create_user(
#             username="application_manager",
#             email="appmanager@sk.cz",
#             roles=["application_manager"],
#             password="pass123",
#         ),
#         security.datastore.create_user(
#             username="admin", email="admin@sk.cz", roles=["admin"], password="pass123"
#         ),
#     ]

#     for user in users:
#         user.save()

#     from app.models.ingredients import Ingredient

#     ingredients = [
#         Ingredient(name="první surovina", created_by=users[0].id),
#         Ingredient(name="druhá surovina", created_by=users[0].id),
#         Ingredient(name="třetí surovina", created_by=users[0].id),
#     ]

#     for ingredient in ingredients:
#         ingredient.save()

#     from app.models.recipes import Recipe

#     recipe = Recipe(
#         name="první recept", created_by=users[0].id, portion_count=1, is_shared=False
#     )
#     recipe.add_ingredient(ingredients[0], amount=20)
#     recipe.add_ingredient(ingredients[2], amount=10)
#     recipe.save()

#     recipe_2 = Recipe(
#         name="veřejný recept", created_by=users[0].id, portion_count=1, is_shared=True
#     )
#     recipe_2.add_ingredient(ingredients[0], amount=20)
#     recipe_2.add_ingredient(ingredients[2], amount=10)
#     recipe_2.save()
