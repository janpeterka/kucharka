from app import security


def create_user(username=None, password=None, roles=[]):
    if not password:
        password = _random_password()

    user_dict = {
        "username": username,
        "password": password,
        "email": _random_email(),
    }

    user = security.datastore.create_user(**user_dict)
    security.datastore.activate_user(user)

    for role in user.roles:
        r = security.datastore.find_or_create_role(role)
        security.datastore.add_role_to_user(user, r)

    return user


def _get_password_hash(password):
    import bcrypt

    if not isinstance(password, bytes) and password is not None:
        password = password.encode("utf-8")

    return bcrypt.hashpw(password, bcrypt.gensalt())


def _random_email(char_num=12):
    import random
    import string

    first_part = "".join(random.choice(string.ascii_letters) for _ in range(char_num))
    last_part = random.choice(["@email.cz", "@gmail.com", "@e.mail"])

    return f"{first_part}{last_part}"


def _random_password(char_num=12):
    import random
    import string

    return "".join(random.choice(string.ascii_letters) for _ in range(char_num))
