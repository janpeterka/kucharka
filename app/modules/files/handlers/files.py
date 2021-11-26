"""
File Handlers

This class is used to manage files.

Currently two types of storage are supported:
    - Local (via LocalFileHandler)
    - AWS (via AWSFileHandler)

    All types should support following public methods:
    - save (expecting File)
    - delete (expecting File)
    - show (expecting File)
    - url (expecting File)
    -
    - @property all_files


expects:
   - Files model for type checking (probably will find a way to change this)
   - Files controller (for generating url. don't know how to do this other way yet.)
"""

import os

from werkzeug.utils import secure_filename

from flask import send_from_directory
from flask import current_app as application


class FileHandler(object):
    def __new__(self, **kwargs):
        if application.config["STORAGE_SYSTEM"] == "LOCAL":
            return LocalFileHandler(**kwargs)
        elif application.config["STORAGE_SYSTEM"] == "AWS":
            return AWSFileHandler(**kwargs)
        else:
            return LocalFileHandler(**kwargs)


class LocalFileHandler(object):
    def __init__(self, subfolder=None):
        self.folder = os.path.join(application.root_path, "files/")
        # create folder `files/` if doesn't exist
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        if subfolder is not None:
            self.folder = os.path.join(self.folder, subfolder)
            # create folder `files/subfolder/` if doesn't exist
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)

        # self.allowed_extension = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

    def save(self, file):
        """
        Arguments:
            file {app.models.File}
        """

        from ..models.files import File

        if isinstance(file, File):
            file.data.name = file.name
            file = file.data

        file.name = secure_filename(file.name)

        file.save(self._get_full_path(file))

        # convert to raw
        # file.data.name = file.name
        # file = file.data

        # print(type(file))
        # print(file.__dict__)

        # self._save_raw(file)

    # def _save_raw(self, raw_file):
    #     """
    #     Arguments:
    #         file {werkzeug.datastructures.FileStorage} --
    #     """
    #     print(f"saving {raw_file} to {self._get_full_path(raw_file)}")
    #     raw_file.name = secure_filename(raw_file.name)
    #     raw_file.save(self._get_full_path(raw_file))

    def delete(self, file):
        """
        Arguments:
            file {app.models.File}
        """
        if os.path.exists(self._get_full_path(file)):
            os.remove(self._get_full_path(file))

    def show(self, file, thumbnail=False):
        if thumbnail is True:
            self.folder = os.path.join(self.folder, "thumbnails/")

        return send_from_directory(self.folder, file.path)

    def url(self, file, thumbnail=False):
        from flask import url_for

        return url_for("FilesView:show", hash_value=file.hash, thumbnail=thumbnail)

    @property
    def all_files(self):
        from ..models.files import File

        file_names = [
            f
            for f in os.listdir(self.folder)
            if os.path.isfile(os.path.join(self.folder, f))
        ]

        files = []

        for file in file_names:
            file = File().load_by_attribute("path", file)
            if file is not None and file.can_current_user_view:
                files.append(file)

        return files

    def _get_full_path(self, file):
        # File.path or FileStorage.name
        name = getattr(file, "path", getattr(file, "name", None))
        return os.path.join(self.folder, name)

    # def download(self, file):
    #     return send_file(file.path, attachment_filename=file.name,)
    #


class AWSFileHandler(object):
    def __init__(self, subfolder=None):
        import boto3

        self.client = boto3.client(
            "s3",
            aws_access_key_id=application.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=application.config["AWS_SECRET_ACCESS_KEY"],
            region_name="eu-west-3",
        )

        self.resource = boto3.resource(
            "s3",
            aws_access_key_id=application.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=application.config["AWS_SECRET_ACCESS_KEY"],
            region_name="eu-west-3",
        )
        self.folder = ""
        if subfolder is not None:
            self.folder = os.path.join(self.folder, subfolder)

        # TODO check if it's needed to add nonexistent subfolder

    def save(self, file):
        folder = LocalFileHandler(subfolder="tmp").folder
        object_name = os.path.join(self.folder, file.name)
        self._upload_file(os.path.join(folder, file.path), object_name)

    def delete(self, file):
        object_name = os.path.join(self.folder, file.full_identifier)
        self.resource.Object(application.config["BUCKET"], object_name).delete()

    def show(self, file):
        raise NotImplementedError

    def url(self, file, thumbnail=False):
        if thumbnail is True:
            file_path = f"thumbnails/{file.path}"
        else:
            file_path = file.path
        return self._create_presigned_url(file_path)

    @property
    def all_files(self):
        from ..models.files import File

        aws_files = self._list_files()
        files = []
        for file in aws_files:
            file = File().load_by_attribute("path", file["Key"])
            if file is not None and file.can_current_user_view:
                files.append(file)

        return files

    # def download_file(self, file_name):
    #     """
    #     Function to download a given file from an S3 bucket
    #     """
    #     output = file_name
    #     self.resource.Bucket(application.config["BUCKET"]).download_file(file_name, output)

    #     return output

    def _upload_file(self, file_path, file_name):
        """
        Function to upload a file to an S3 bucket
        """
        response = self.client.upload_file(
            file_path, application.config["BUCKET"], file_name
        )

        return response

    def _list_files(self):
        """
        Function to list files in a given S3 bucket
        """
        contents = []
        try:
            for item in self.client.list_objects(Bucket=application.config["BUCKET"])[
                "Contents"
            ]:
                contents.append(item)
        except Exception:
            return []

        return contents

    def _create_presigned_url(self, file_path, expiration=3600):
        from botocore.exceptions import ClientError

        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        object_name = file_path
        try:
            response = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": application.config["BUCKET"], "Key": object_name},
                ExpiresIn=expiration,
            )
        except ClientError:
            return None

        # The response contains the presigned URL
        return response


class ImageHandler(object):
    def __new__(self, **kwargs):
        if application.config["STORAGE_SYSTEM"] == "LOCAL":
            return LocalImageHandler(**kwargs)
        elif application.config["STORAGE_SYSTEM"] == "AWS":
            return AWSImageHandler(**kwargs)
        else:
            return LocalImageHandler(**kwargs)


class ImageHandlerMixin(object):
    def delete(self, file):
        FileHandler().delete(file)
        FileHandler(subfolder="thumbnails").delete(file)

    def create_thumbnail(self, file, file_path, size):
        from PIL import Image

        image = Image.open(file_path)
        image.thumbnail(size)
        image.name = file.name

        return image


class LocalImageHandler(ImageHandlerMixin):
    def create_and_save_with_thumbnail(self, file, size=(128, 128)):
        # save file
        LocalFileHandler().save(file)
        file_path = LocalFileHandler()._get_full_path(file)

        thumbnail = self.create_thumbnail(file, file_path, size)

        LocalFileHandler(subfolder="thumbnails").save(thumbnail)


class AWSImageHandler(ImageHandlerMixin):
    def create_and_save_with_thumbnail(self, file, size=(128, 128)):
        # save to temporary
        fh = LocalFileHandler(subfolder="tmp")
        fh.save(file)
        file_path = fh._get_full_path(file)

        # save file to AWS
        FileHandler().save(file)

        # create and save thumbnail (rewriting original tmp?)
        thumbnail = self.create_thumbnail(file, file_path, size)
        thumbnail.path = file.name
        fh.save(thumbnail)

        # save thumbnail file to AWS
        FileHandler(subfolder="thumbnails").save(thumbnail)

        fh.delete(file)
        fh.delete(thumbnail)
