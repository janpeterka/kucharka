def camelcase_to_snakecase(text: str) -> str:
    import re

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
