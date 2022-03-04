def db_fill():
    # from flask_security import create_user, create_role
    from app import security

    roles = [
        security.datastore.create_role(
            name="admin",
            permissions="manage-application,manage-users,login-as,see-debug,see-other,edit-other",
        ),
        security.datastore.create_role(
            name="application_manager",
            permissions="manage-application,see-other,edit-other",
        ),
    ]

    for role in roles:
        role.save()

    users = [
        security.datastore.create_user(
            username="user", email="user@sk.cz", password="pass123"
        ),
        security.datastore.create_user(
            username="application_manager",
            email="appmanager@sk.cz",
            roles=["application_manager"],
            password="pass123",
        ),
        security.datastore.create_user(
            username="admin", email="admin@sk.cz", roles=["admin"], password="pass123"
        ),
    ]

    for user in users:
        user.save()

    print(users[0])

    from app.models.ingredients import Ingredient

    ingredients = [
        Ingredient(name="první surovina", created_by=users[0].id),
        Ingredient(name="druhá surovina", created_by=users[0].id),
        Ingredient(name="třetí surovina", created_by=users[0].id),
    ]

    for ingredient in ingredients:
        ingredient.save()

    from app.models.recipes import Recipe

    recipe = Recipe(
        name="první recept", created_by=users[0].id, portion_count=1, is_shared=False
    )
    recipe.add_ingredient(ingredients[0], amount=20)
    recipe.add_ingredient(ingredients[2], amount=10)
    recipe.save()

    recipe_2 = Recipe(
        name="veřejný recept", created_by=users[0].id, portion_count=1, is_shared=True
    )
    recipe_2.add_ingredient(ingredients[0], amount=20)
    recipe_2.add_ingredient(ingredients[2], amount=10)
    recipe_2.save()
