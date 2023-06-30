class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def empty_object(**kwargs):
    import types

    return types.SimpleNamespace(**kwargs)


def list_without_duplicated(array) -> list:
    # res = []
    # [res.append(x) for x in array if x not in res]
    # return res

    return list(dict.fromkeys(array))


def listify(obj_or_list) -> list:
    from sqlalchemy.ext.associationproxy import _AssociationList

    # check if it is instance list or subclass of list (e.g. SQLAlchemy InstrumentedList)

    if type(obj_or_list) in [list, _AssociationList] or issubclass(
        type(obj_or_list), list
    ):
        return obj_or_list
    else:
        return [obj_or_list]


def flatten(array) -> list:
    return [item for sublist in array for item in sublist]


def power_flatten(array) -> list:
    while has_sublists(array):
        array = flatten(array)


def has_sublists(array) -> bool:
    return bool([item for item in array if type(item) == list])


def slugify(value, allow_unicode=False):
    import unicodedata
    import re

    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def obscure(data: bytes) -> bytes:
    import zlib
    from base64 import urlsafe_b64encode as b64e

    return b64e(zlib.compress(data, 9))


def unobscure(obscured: bytes) -> bytes:
    import zlib
    from base64 import urlsafe_b64decode as b64d

    return zlib.decompress(b64d(obscured))
