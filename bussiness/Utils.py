# coding: utf-8

import os
from typing import Union


def get_icon(rel_path: str) -> Union[str, None]:
    full_path: str = os.path.join(os.getcwd(), "assets", rel_path)
    return full_path if os.path.isfile(full_path) else None
