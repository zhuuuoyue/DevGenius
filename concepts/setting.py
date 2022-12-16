# coding: utf-8

from typing import Optional, Union


class FileAuthors(object):

    def __init__(self, owner: Optional[str] = None, co_owner: Optional[str] = None):
        self.owner: Union[str, None] = owner
        self.co_owner: Union[str, None] = co_owner
