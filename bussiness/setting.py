# coding: utf-8

from concepts.setting import FileAuthors
from db.setting import get_setting, SettingKey


def get_authors() -> FileAuthors:
    setting = get_setting()
    return FileAuthors(
        owner=setting.get(SettingKey.OWNER),
        co_owner=setting.get(SettingKey.CO_OWNER)
    )


def set_authors(authors: FileAuthors) -> None:
    setting = get_setting()
    setting.update({
        SettingKey.OWNER: authors.owner,
        SettingKey.CO_OWNER: authors.co_owner
    })
