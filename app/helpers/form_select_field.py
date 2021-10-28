from wtforms_sqlalchemy.fields import QuerySelectField

# from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields import SelectFieldBase


class SelectFieldBase(SelectFieldBase):
    def __iter__(self):
        opts = dict(
            widget=self.option_widget, _name=self.name, _form=None, _meta=self.meta
        )
        for i, (value, label, checked) in enumerate(self.iter_choices()):
            opt = self._Option(label=label, id="%s-%d" % (self.id, i), **opts)
            opt.process(None, value)
            opt.checked = checked
            yield opt


class MyQuerySelectField(QuerySelectField):
    def iter_choices(self):
        if self.allow_blank:
            yield (
                "__None",
                self.blank_text,
                self.data is None,
            )

        for pk, obj in self._get_object_list():
            yield (pk, self.get_label(obj), obj == self.data)
