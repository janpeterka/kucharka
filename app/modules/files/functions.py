#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .handlers import FileHandler


def show_file(file, thumbnail):
    return FileHandler().show(file, thumbnail=thumbnail)


def download_file(file):
    return FileHandler().download(file)


def all_files():
    return FileHandler().all_files
