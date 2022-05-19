class BasePresenter:
    def __str__(self):
        if hasattr(self, "name"):
            return self.name
        else:
            return self.__str__
