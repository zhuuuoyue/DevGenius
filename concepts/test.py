# coding: utf-8

import datetime
import os.path
from enum import Enum
from typing import Union, Optional


class TestCaseRunningStatus(Enum):

    Unknown = 0
    Passed = 1
    Failed = 2


class TestCaseRunningError(object):

    def __init__(self,
                 name: Optional[str] = None,
                 task_id: Optional[int] = None,
                 filename: Optional[str] = None,
                 line_number: Optional[int] = None,
                 function: Optional[str] = None,
                 message: Optional[str] = None,
                 author: Optional[str] = None,
                 date: Optional[datetime.date] = None,
                 *args,
                 **kwargs):
        self.name: Union[str, None] = name
        self.task_id: Union[int, None] = task_id
        self.filename: Union[str, None] = filename
        self.line_number: Union[int, None] = line_number
        self.function: Union[str, None] = function
        self.message: Union[str, None] = message
        self.author: Union[str, None] = author
        self.date: Union[datetime.date, None] = date


class TestCase(object):

    def __init__(self,
                 group: Union[str] = None,
                 name: Optional[str] = None,
                 run_time_limited: Optional[int] = None,
                 run_speed: Optional[int] = None,
                 count: Optional[int] = None,
                 debug_mode: Optional[str] = None,
                 js_filename: Optional[str] = None,
                 to_run: Optional[bool] = None,
                 run_type: Optional[str] = None,
                 exe_name: Optional[str] = None,
                 depend_on_source: Optional[bool] = None,
                 directory: Optional[str] = None,
                 *args,
                 **kwargs):
        self.group: Union[str, None] = group
        self.name: Union[str, None] = name
        self.run_time_limited: Union[int, None] = run_time_limited
        self.run_speed: Union[int, None] = run_speed
        self.count: Union[int, None] = count
        self.debug_mode: Union[str, None] = debug_mode
        self.js_filename: Union[str, None] = js_filename
        self.to_run: Union[bool, None] = to_run
        self.run_type: Union[str, None] = run_type
        self.exe_name: Union[str, None] = exe_name
        self.depend_on_source: Union[bool, None] = depend_on_source
        self.directory: Union[str, None] = directory


class TestCaseRunningResult(object):

    def __init__(self,
                 status: Optional[str] = None,
                 output_directory: Optional[str] = None,
                 cost_seconds: Optional[float] = None,
                 test_case: Optional[TestCase] = None,
                 *args,
                 **kwargs):
        self.status: Union[str, None] = status
        self.output_directory: Union[str, None] = output_directory
        self.test_case: Union[TestCase, None] = test_case
        self.cost_seconds: Union[float, None] = cost_seconds
        self.error_info: Union[TestCaseRunningError, None] = None


class TestCaseRunningResultCollection(object):

    def __init__(self):
        self.__list: list[TestCaseRunningResult] = []
        self.__map: dict[str, TestCaseRunningResult] = {}
        self.output_directory: Union[str, None] = None
        self.ini_filename: Union[str, None] = None
        self.html_filename: Union[str, None] = None

    def add_item(self, item: TestCaseRunningResult) -> bool:
        if not isinstance(item, TestCaseRunningResult):
            return False
        if not isinstance(item.test_case, TestCase):
            return False
        name = item.test_case.name
        basename, ext = os.path.splitext(name)
        self.__list.append(item)
        self.__map[basename] = item
        return True

    def get_item_by_name(self, name: str) -> Union[TestCaseRunningResult, None]:
        if not isinstance(name, str):
            return None
        if name not in self.__map:
            return None
        return self.__map[name]

    def get_item_by_index(self, index: int) -> Union[TestCaseRunningResult, None]:
        if not isinstance(index, int):
            return None
        if index < 0 or index >= len(self.__list):
            return None
        return self.__list[index]

    def get_count(self) -> int:
        return len(self.__list)

    def get_data(self) -> list[TestCaseRunningResult]:
        return self.__list

    data = property(get_data)
