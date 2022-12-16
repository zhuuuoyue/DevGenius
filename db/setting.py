# coding: utf-8

import os
import json
from typing import Any


class SettingKey(object):

    OWNER: str = "owner"
    CO_OWNER: str = "co_owner"


class Setting(object):

    def __init__(self):
        self.__data: dict[str, Any] = {
            SettingKey.OWNER: u"",
            SettingKey.CO_OWNER: u""
        }

    @staticmethod
    def get_setting_filename() -> str:
        return os.path.join(os.getcwd(), u"settings.json")

    def load(self) -> None:
        filename = Setting.get_setting_filename()
        if not isinstance(filename, str):
            return
        if not os.path.isfile(filename):
            return
        with open(filename, "r", encoding="utf-8") as fp:
            loaded = json.load(fp)
            self.__data.update(loaded)

    def save(self) -> None:
        filename = Setting.get_setting_filename()
        directory = os.path.dirname(filename)
        if not os.path.isdir(directory):
            return
        with open(filename, "w", encoding="utf-8") as fp:
            json.dump(obj=self.__data, fp=fp, indent=4)

    def has(self, key: str) -> bool:
        return key in self.__data

    def get(self, key: str) -> Any:
        return self.__data[key] if self.has(key) else None

    def set(self, key: str, value: Any) -> None:
        self.__data[key] = value
        self.save()

    def update(self, params: dict[str, Any]) -> None:
        self.__data.update(params)
        self.save()


_setting: Setting = Setting()
_setting.load()


def get_setting() -> Setting:
    return _setting
