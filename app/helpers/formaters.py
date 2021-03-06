import datetime


# private
def parse_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()


def coma_to_float(string):
    if string is None:
        return None
    string = string.replace(",", ".")
    try:
        return float(string)
    except Exception:
        return None


def string_to_list(string):
    string = string.replace("[", "").replace("]", "")
    array = string.split(",")
    array = [x.strip() for x in array]
    return array


def week_day(date):
    weekdays = ("pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")
    try:
        return weekdays[date.weekday()]
    except Exception:
        raise AttributeError(f"Date {date} doesn't have weekday")
