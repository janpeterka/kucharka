from flask import g


class DataHandler:
    @staticmethod
    def set_additional_request_data(**kwargs):
        for key, value in kwargs.items():
            setattr(g, key, value)

    @staticmethod
    def get_additional_request_data(key):
        return getattr(g, key, None)
