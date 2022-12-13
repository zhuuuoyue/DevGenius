# coding: utf-8

from typing import Union, Optional


class DbgWarnInfo(object):

    def __init__(self, task_id: Optional[int] = None, filename: Optional[str] = None, line_number: Optional[int] = None,
                 function: Optional[str] = None, message: Optional[str] = None, author: Optional[str] = None,
                 date: Optional[str] = None):
        self.task_id = None
        self.filename = None
        self.line_number = None
        self.function = None
        self.message = None
        self.author = None
        self.date = None

        self.task_id = task_id
        self.filename = filename
        self.line_number = line_number
        self.function = function
        self.message = message
        self.author = author
        self.date = date

    def is_valid(self) -> bool:
        pass

    # def get_task_id(self) -> Union[int, None]:
    #     return self.__task_id
    #
    # def set_task_id(self, task_id: int) -> None:
    #     if isinstance(task_id, int):
    #         self.__task_id = task_id
    #
    # task_id = property(get_task_id, set_task_id)


class TestCase(object):

    def __init__(self, name: Optional[str] = None, js_filename: Optional[str] = None,
                 error: Optional[DbgWarnInfo] = None):
        self.name = None
        self.js_filename = None
        self.error = None

        self.name = name
        self.js_filename = js_filename
        self.error = error
