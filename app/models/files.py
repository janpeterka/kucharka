import os
from werkzeug.utils import secure_filename

from flask_login import current_user

from app import db

from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter

from app.modules.files import FileHandler, ImageHandler


class File(db.Model, BaseMixin, BasePresenter):
    __tablename__ = "files"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )

    user_id = db.Column(db.ForeignKey("users.id"))
    recipe_id = db.Column(db.ForeignKey("recipes.id"))

    created_by = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)

    file_type = db.Column(db.String(40))

    author = db.relationship(
        "User",
        primaryjoin="File.created_by == User.id",
        backref="files",
    )

    __mapper_args__ = {"polymorphic_on": file_type, "polymorphic_identity": "file"}

    subfolder = ""

    def save(self, with_thumbnail=True):
        # converts "some.picture.jpg" to "some.picture"
        self.name = secure_filename(".".join(self.data.filename.split(".")[:-1]))
        # converts "some.picture.jpg" to "jpg"
        self.extension = secure_filename(".".join(self.data.filename.split(".")[-1:]))
        self.path = os.path.join(self.subfolder, f"{self.name}.{self.extension}")

        if getattr(self, "created_by", None) is None:
            self.created_by = current_user.id

        # hash cannot be empty, but real will be created after path
        self.hash = ""

        super().save()

        # rename to match db id
        self._rename_to_id()
        self.hash = self._get_hash_from_path()
        super().edit()

        # save file
        self.name = f"{self.id}.{self.extension}"
        if with_thumbnail:
            self._add_thumbnail()
        else:
            FileHandler().save(self)

        self.expire()

        return self

    def _get_hash_from_path(self):
        from hashlib import md5

        return md5(self.path.encode("utf-8")).hexdigest()  # nosec

    def _rename_to_id(self):
        self.path = os.path.join(self.subfolder, f"{self.id}.{self.extension}")
        super().edit()
        return self

    def _add_thumbnail(self):
        ImageHandler().create_and_save_with_thumbnail(self)

    def delete(self):
        ImageHandler().delete(self)
        super().delete()

    @property
    def url(self):
        return FileHandler().url(self)

    @property
    def thumbnail_url(self):
        return FileHandler().url(self, thumbnail=True)

    @property
    def full_name(self):
        return f"{self.name}.{self.extension}"

    @property
    def full_identifier(self):
        return f"{self.id}.{self.extension}"

    @property
    def object(self):
        raise NotImplementedError


class ImageFile(File):
    __mapper_args__ = {"polymorphic_identity": "image"}


class RecipeImageFile(ImageFile):
    __mapper_args__ = {"polymorphic_identity": "recipe_image"}

    is_main = db.Column(db.Boolean(), default=False)

    recipe = db.relationship(
        "Recipe",
        primaryjoin="RecipeImageFile.recipe_id == Recipe.id",
        backref="images",
    )

    @property
    def is_public(self) -> bool:
        return self.recipe.is_public

    @property
    def object(self):
        return self.recipe
