from app import db
from flask import current_app as application


class CalendarUserMixin:
    calendar_hash = db.Column(db.String(255), unique=True)

    @staticmethod
    def load_by_calendar_hash(hash_value):
        from app.models.users import User

        return User.load_by_attribute("calendar_hash", hash_value)

    def set_calendar_hash(self, hash_function=None):
        if not hash_function:
            hash_function = self._generate_calendar_hash

        self.calendar_hash = hash_function()
        self.save()

    def _generate_calendar_hash(self):
        from hashlib import md5
        from datetime import datetime

        data_to_hash = f"{self.id}:{application.config['SECRET_KEY']}:{datetime.now()}"
        return md5(data_to_hash.encode("utf-8")).hexdigest()  # nosec
