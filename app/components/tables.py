import random
from flask import render_template
from markupsafe import Markup
from kucharka.packages.template_components import BaseComponent

from app.helpers.general import listify


class TableComponent(BaseComponent):
    folder = "tables"


class Table(TableComponent):
    file = "table"


class TableHeader(TableComponent):
    file = "header"


class TableBody(TableComponent):
    file = "body"


class TableRow(TableComponent):
    file = "row"


def table(objects, attribute_names, use_default_kwargs=True, table_kwargs={}, **kwargs):
    """Table generator

    Expects list of objects and attributes to render.
    Attributes are then translated to header values by presented table_columns.

    Example usage:
        table(tasks, ["name", "due_date", "reminder_date"])
    """
    DEFAULT_BS_TABLE_KWARGS = {
        "data-toggle": "table",
        "data-search": "true",
        "data-search-selector": "#search_box",
        "data-classes": "table table-hover table-borderless table-responsive-lg",
        "data-controller": "enable-table",
    }
    klass = kwargs.get("class", None)

    # this section handles setting column names shown in table header
    if objects and hasattr(objects[0].__class__, "table_columns"):
        # first we try to get them from object class, if there is any object
        column_names = [
            objects[0].__class__.table_columns.get(key, key) for key in attribute_names
        ]
    elif klass and hasattr(klass, "table_columns"):
        # second way is to get them from class, given in kwargs
        column_names = [klass.table_columns.get(key, key) for key in attribute_names]
    else:
        # if there are no objects and no class, fallback is to use default translation dictionary directly
        from app.presenters.common.translations import translations

        column_names = [translations.get(key, key) for key in attribute_names]

    if use_default_kwargs:
        table_kwargs = {**DEFAULT_BS_TABLE_KWARGS, **table_kwargs}

    return Table(
        objects=objects,
        column_names=column_names,
        attribute_names=attribute_names,
        table_kwargs=table_kwargs,
    ).render()


def table_header(column_names):
    """Table header (`<thead>`) generator

    Example usage:
        table_header(["název", "datum do", "připomínka"])
    """
    return TableHeader(column_names=column_names).render()


def table_body(objects, attribute_names):
    """Table body (`<tbody>`) generator

    Example usage:
        table_body(tasks, ["name", "due_date", "reminder_date"])
    """
    rows = [table_row(obj, attribute_names=attribute_names) for obj in objects]

    return TableBody(rows=rows).render()


def table_row(obj=None, /, **kwargs):
    # I tried to place this in args/kwargs, but it behaved badly.

    column_values = kwargs.pop("column_values", [])
    attribute_names = kwargs.pop("attribute_names", [])

    if column_values:
        return TableRow(column_values=column_values).render()
    elif attribute_names and obj:
        for attribute in attribute_names:
            if hasattr(obj, f"table_col_{attribute}"):
                column_values.append(getattr(obj, f"table_col_{attribute}"))
            elif hasattr(obj, attribute):
                column_values.append(getattr(obj, attribute))
            else:
                raise AttributeError(
                    f'Object {obj} has neither "table_col_{attribute}" (defined in presenter) nor "{attribute}" attribute.\n'
                )

        return TableRow(column_values=column_values).render()
    else:
        raise AttributeError(
            "You need to provide either `column_values` or `attribute_names` and `obj` attributes for this to work."
        )


def search_box(suggestions=None, suggestion_attributes=["name"]):
    suggestion_attributes = listify(suggestion_attributes)
    suggestion_texts = []
    if suggestions:
        for obj in suggestions:
            for attr in suggestion_attributes:
                if hasattr(obj, attr):
                    suggestion_texts.append(getattr(obj, attr))

    if suggestion_texts:
        suggestion = random.choice(suggestion_texts)  # nosec
    else:
        suggestion = None

    return Markup(
        render_template(
            "template_components/tables/search_box.html.j2", suggestion=suggestion
        )
    )
