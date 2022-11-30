# coding: utf-8

from typing import Sequence

from concepts import Repository


def get_repositories() -> list[Repository]:
    """Get all repositories recorded.

    Returns:
        Repository list.
    """
    return [
        Repository("D:\\gap"),
        Repository("E:\\gap"),
        Repository("F:\\gap")
    ]
