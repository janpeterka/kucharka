def empty_object():
    import types

    return types.SimpleNamespace()


def list_without_duplicated(array) -> list:
    return list(dict.fromkeys(array))


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


def placeholder_day(date):
    from app.helpers.formaters import week_day

    day = empty_object()
    day.date = date
    day.weekday = week_day(date)
    return day
