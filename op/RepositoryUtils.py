# coding: utf-8

from typing import Sequence

from concepts import Repository


def get_repositories() -> list[Repository]:
    return [
        Repository("D:\\gap"),
        Repository("E:\\gap"),
        Repository("F:\\gap")
    ]
