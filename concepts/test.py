# coding: utf-8

from datetime import date as Date
from typing import Union, Optional


class DbgWarnInfo(object):

    def __init__(self, task_id: Optional[int] = None, filename: Optional[str] = None, line_number: Optional[int] = None,
                 function: Optional[str] = None, message: Optional[str] = None, author: Optional[str] = None,
                 date: Optional[Date] = None):
        self.__task_id = None
        self.__filename = None
        self.__line_number = None
        self.__function = None
        self.__message = None
        self.__author = None
        self.__date = None

        self.task_id = task_id
        self.filename = filename
        self.line_number = line_number
        self.function = function
        self.message = message
        self.author = author
        self.date = date

    def is_valid(self) -> bool:
        pass

    def get_task_id(self) -> Union[int, None]:
        return self.__task_id

    def set_task_id(self, task_id: int) -> None:
        if isinstance(task_id, int):
            self.__task_id = task_id

    task_id = property(get_task_id, set_task_id)

    def get_filename(self) -> Union[str, None]:
        return self.__filename

    def set_filename(self, filename: Union[str, None]) -> None:
        if filename is None or isinstance(filename, str):
            self.__filename = filename

    filename = property(get_filename, set_filename)

    def get_line_number(self) -> Union[int, None]:
        return self.__line_number

    def set_line_number(self, line_number: Union[int, None]) -> None:
        if line_number is None or isinstance(line_number, int):
            self.__line_number = line_number

    line_number = property(get_line_number, set_line_number)

    def get_function(self) -> Union[str, None]:
        return self.__function

    def set_function(self, function: Union[str, None]) -> None:
        if function is None or isinstance(function, str):
            self.__function = function

    function = property(get_function, set_function)

    def get_message(self) -> Union[str, None]:
        return self.__message

    def set_message(self, message: Union[str, None]) -> None:
        if message is None or isinstance(message, str):
            self.__message = message

    message = property(get_message, set_message)

    def get_author(self) -> Union[str, None]:
        return self.__author

    def set_author(self, author: Union[str, None]) -> None:
        if author is None or isinstance(author, str):
            self.__author = author

    author = property(get_author, set_author)

    def get_date(self) -> Union[Date, None]:
        return self.__date

    def set_date(self, value: Union[Date, None]) -> None:
        if value is None or isinstance(value, Date):
            self.__date = value

    date = property(get_date, set_date)


class TestCase(object):

    def __init__(self, name: Optional[str] = None, js_filename: Optional[str] = None, directory: Optional[str] = None,
                 error: Optional[DbgWarnInfo] = None):
        self.__name = None
        self.__js_filename = None
        self.__directory = None
        self.__error = None

        self.name = name
        self.js_filename = js_filename
        self.directory = directory
        self.error = error

    def get_name(self) -> Union[str, None]:
        return self.__name

    def set_name(self, name: Union[str, None]) -> None:
        if name is None or isinstance(name, str):
            self.__name = name

    name = property(get_name, set_name)

    def get_js_filename(self) -> Union[str, None]:
        return self.__js_filename

    def set_js_filename(self, js_filename: Union[str, None]) -> None:
        if js_filename is None or isinstance(js_filename, str):
            self.__js_filename = js_filename

    js_filename = property(get_js_filename, set_js_filename)

    def get_directory(self) -> Union[str, None]:
        return self.__directory

    def set_directory(self, directory: Union[str, None]) -> None:
        if directory is None or isinstance(directory, str):
            self.__directory = directory

    directory = property(get_directory, set_directory)

    def get_error(self) -> Union[DbgWarnInfo, None]:
        return self.__error

    def set_error(self, error: Union[DbgWarnInfo, None]) -> None:
        if error is None or isinstance(error, DbgWarnInfo):
            self.__error = error

    error = property(get_error, set_error)
