from flask import url_for, redirect
from app import turbo


class AdminViewMixin:
    def show_edit(self):
        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.after(
                        self.template(template_name="_edit"),
                        target=f"{self._attribute_name}-{self._instance.id}",
                    ),
                    turbo.replace(
                        self.template(template_name="_row", editing=True),
                        target=f"{self._attribute_name}-{self._instance.id}",
                    ),
                ]
            )
        else:
            return redirect(url_for(f"{self.name}:index", edit_id=self._instance.id))

    def hide_edit(self):
        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.remove(
                        target=f"{self._attribute_name}-edit-{self._instance.id}",
                    ),
                    turbo.replace(
                        self.template(template_name="_row"),
                        target=f"{self._attribute_name}-{self._instance.id}",
                    ),
                ]
            )
        else:
            return redirect(url_for(f"{self.name}:index"))

    def post_edit(self):
        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.replace(
                        self.template(template_name="_row"),
                        target=f"{self._attribute_name}-{self._instance.id}",
                    ),
                    turbo.remove(
                        target=f"{self._attribute_name}-edit-{self._instance.id}"
                    ),
                ]
            )
        else:
            return redirect(url_for(f"{self.name}:index"))

    def post(self):
        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.append(
                        self.template(template_name="_row"),
                        target=f"{self._attribute_name}s",
                    ),
                    turbo.replace(
                        self.template(template_name="_add"),
                        target=f"{self._attribute_name}-create-form",
                    ),
                ]
            )
        else:
            return redirect(url_for(f"{self.name}:index"))

    def delete(self):
        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.remove(target=f"{self._attribute_name}-{self._instance.id}"),
                    turbo.remove(
                        target=f"{self._attribute_name}-edit-{self._instance.id}"
                    ),
                ]
            )
        else:
            return redirect(url_for(f"{self.name}:index"))

    @property
    def _model_name(self):
        # e.g. Measurement
        if type(self).__name__.endswith("sView"):
            model_name = type(self).__name__.replace("sView", "")
        elif type(self).__name__.endswith("View"):
            model_name = type(self).__name__.replace("View", "")
        else:
            raise AttributeError("self name not ending with 'View'")

        return model_name

    @property
    def _attribute_name(self):
        import re

        # e.g. measurement
        model_name = self._model_name
        return re.sub("(?!^)([A-Z]+)", r"_\1", model_name).lower()

    @property
    def _instance(self):
        instance = getattr(self, self._attribute_name)
        return instance
