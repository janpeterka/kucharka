from app.data.template_data import texts


class objdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


texts = objdict(texts)

# Solve nested
for attribute in texts:
    value = getattr(texts, attribute)
    if type(value) == dict:
        setattr(texts, attribute, objdict(value))
