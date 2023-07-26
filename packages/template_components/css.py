from typing import Union


class CSSClasses:
    def __init__(self, initial_classes: Union[str, list[str]] = None):
        self.classes = ""
        self.append(initial_classes)

    def __str__(self):
        return self.classes

    def append(self, new_classes: Union[str, list[str]]):
        """Add css classes to class list

        [description]

        Examples:
        - self.css_classes.append("btn")
        - self.css_classes.append("btn btn-primary")
        - self.css_classes.append(["btn", "btn-primary"])

        :param new_classes: css classes to add
        :type new_classes: Union[str, list[str]]
        :raises: TypeError
        """
        if isinstance(new_classes, list):
            new_classes = " ".join(new_classes)
        elif isinstance(new_classes, str):
            new_classes = new_classes.strip()
        else:
            raise TypeError("New classes must be a string.")

        if self.classes:
            self.classes += f" {new_classes}"
        else:
            self.classes = new_classes
