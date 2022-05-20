class BasePresenter:
    def __str__(self):
        return self.name if hasattr(self, "name") else self.__str__
