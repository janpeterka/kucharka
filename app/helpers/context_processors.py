def human_format_date(date, with_weekday=True, with_relative=True):
    import datetime

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

    return formatted_date


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


def link_to(obj, **kwargs):
    try:
        return obj.link_to(**kwargs)
    except Exception:
        raise NotImplementedError(
            f"{obj}({obj.__class__}) doesn't have `link_to` implemented"
        )


def link_to_edit(obj, **kwargs):
    try:
        return obj.link_to_edit(**kwargs)
    except Exception:
        raise NotImplementedError(
            f"{obj}({obj.__class__}) doesn't have `link_to_edit` implemented"
        )
