class DailyPlanRecipeMixin:

    # PROPERTIES

    @property
    def real_recipes(self):
        return [r for r in self.recipes if not r.is_shopping]
