# What's Flask-TemplateComponents purpose?
Are you too lazy to write the same HTML over and over again?
Do you find Jinja powerful, but not very readable in complex cases?

## Basic philosophy

### Components
Core of TemplateComponents is (you guessed it) Component classes.
These can be anything from general `Link`, `Button` or `Image`, through more specific as `ProfilePicture` or `ActionBadge`, those linked to how your application operates as `LinkTo(some_object)` to highly specialized for you use-case, as `WibblyButton`.

All components inherit from `BaseComponent` class, of which we will talk later in more detail.

Components are mostly meant for setting some default visuals and renderings, but are not meant for usage in templates themselves. For that, we have `helpers`:

### helpers
`helpers` are simple wrappings that are meant for usage in templates. So, if you have for example component `WibblyButton`, in template you just call `wibbly_button` helper.
Well, not like this - you want to give some arguments to that button for sure.

### example
Ok, let's see our `WibblyButton` example in some more detail:

For now, we often do something like this in our templates:
```jinja
<button class="btn btn-color-green m-2 animation-wibblyness">{{ button_text }}</button>
```

And now you decided you want to change your button visual. Bit complicated, right? Especially as some wibbly buttons have some added classes, some have data-attributes and whatnot.
> Note: if you are styling your wibbly button just with `wibbly-button` class, in this case Components don't help you that much. But read on, maybe you will find some nice examples why they make sense even for you!

So, what about if you used TemplateComponents from beginning?

You want a `WibblyButton` component, as you often create _wibbly button_. How to do that?


```python
# app/components/buttons.py
from flask_template_components.components import Button


class WibblyButton(Button):
    DEFAULT_CLASSES = ["btn", "btn-color-green", "m-2", "animation-wibblyness"]
```
Ok, this part is (I hope) pretty obvious - we create our custom Component, inheriting from `Button` component from library, and setting our default css classes for this component.

How do we use it now?
There are several ways:

#### Use the component class directly
We can do simply this
```python
# app/routes.py
from flask import render_template
from app.components.buttons import WibblyButton


def route_to_wibbly_button():
    button_text = "text"
    wibbly_button_html = WibblyButton(button_text).render()
    # wibbly_button_html
    return render_template("wibbly_template.html.j2", button=wibbly_button_html)
```
This right here gives us `Markup` data to render in template, test, or do anything with - in your template `button` will be:
```html
<button class="btn btn-color-green m-2 animation-wibblyness">text</button>
```

But usually, you don't want to create html elements in view, right? So, how do we get this in template?
Like this:
```jinja
{{ wibbly_button("text") }}
```

Wait, wait, how does that work? We didn't specify anywere that `wibbly_button` is something we can use in our template, we didn't told it what arguments it accepts or anything! What kind of sorcery is this?

Well, I've hidden few steps from you:

1. If you look into how `Button` is defined, you will find out it expects `value` as first attribute, because button should always have value specified.
2. Delving deeper, every class based on BaseComponent automatically has method `register_helper`, which creates template helpers for us to use (more on that in _How to use this library?_).

So here we are, just by creating our class `WibblyButton` (and a little code that we will look into later), we can suddenly render out _wibbly button_ with ease in templates.

## What does it provide?

### BaseComponent
`css_classes`
`render()`
`helper()`
`register_helper()`

### Pre-made components


# How do I use this library?

## Add to your project
```python
# __init__.py
from flask import Flask
from flask_template_component import TemplateComponents

components = TemplateComponents()


def create_app():
    application = Flask()
    # (...)
    components.init_app(application)
```

## Register included helpers (optional)

```python
# app/__init__.py
from flask import Flask
from flask_template_component import TemplateComponents

components = TemplateComponents()


def create_app():
    application = Flask()
    # (...)
    components.init_app(application)

    components.register_helpers()
```

## Create custom components (optional)
You can do this many ways, here is recommanded way to do this:
```
myapp/
|-- app/
|   |-- components/
|   |   |-- __init__.py
|   |   |-- buttons.py
|   |
|   |-- static/
|   |-- templates/
|   |-- __init__.py
```
To have all components easily accessible for usage, have them importable from `app.components`
```python
# app/components/__init__.py

from .buttons import WibblyButton
```

### Create custom helpers for included or custom-made components (optional)

You can register your custom components helper (`wibbly_button`) by calling (for example) `WibblyButton.register_helper(application)` anywhere.
It's recommanded to do this in one place, I do it like this:

```python
# app/components/__init__.py
from .buttons import WibblyButton
# (...)


def register_helpers(application):
    WibblyButton.register_helper(application)
    # (...)
```

and then call the `register_helpers` when creating my app:
```python
# app/__init__.py
from flask import Flask


def create_app():
    application = Flask()

    from app.components import register_helpers as register_custom_helpers

    register_custom_helpers(application)
```

If you want to create custom helper yourself, you can!

Define your helper function:
```python
# app/components/buttons.py
from flask_template_components.components import Button


def wobbly_button(value, wobbliness=1, **kwargs):
    if wobbliness > 0.5:
        kwargs["classes"] = "animation-wobblyness"

    return Button(value, **kwargs).render()
```

and register it in `register_helpers`:
```python
# app/components/__init__.py
from .buttons import WibblyButton, wobbly_button
# (...)


def register_helpers(application):
    # this will create `wibbly_button`
    WibblyButton.register_helper(application)

    # you can also call this, if you want other name then components
    # WibblyButton.register_helper(application, "wibblybutt")

    application.add_template_global(wobbly_button)
```

