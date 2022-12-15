# coding: utf-8

import os
import re
import datetime
import configparser
from typing import Union, Optional


from concepts.test import TestCase, TestCaseRunningError, TestCaseRunningResult, TestCaseRunningResultCollection


__TOTAL_RESULT_FILENAME = u"TotalResult.html"
__ERROR_TEST_COLLECTION_FILENAME = u"ErrorTestCollection.ini"

__PAT_TOTAL_RESULT_P = re.compile(r"^<p\sstyle='color:(green|red)+;'>(.*)<\/p>$")
__PAT_TOTAL_RESULT_PASSED = re.compile(r"^\"?(.*)：(.*)\(耗时：(\d+\.\d+)s\)\"?$")
__PAT_TOTAL_RESULT_ERROR = re.compile(
    r"^\"?(.*)：<a\shref=\"file:\/\/\/(.*)\"\starget=\"_blank\">(.*)\(耗时：(\d+\.\d+)s\)<\/a>\"?$"
)


def parse_test_result(directory: str, result: TestCaseRunningResultCollection):
    if not os.path.isdir(directory):
        return
    basename = os.path.basename(directory)
    result_item = result.get_item_by_name(basename)
    if basename is None:
        return
    items = os.listdir(directory)
    for item in items:
        if item.endswith(".js") and not item.endswith("_full.js"):
            path = os.path.join(directory, item)
            with open(path, "r", encoding="utf-8") as fp:
                lines = fp.readlines()
                for line in lines:
                    matched = re.match(r"^\/\/\[([a-zA-Z0-9_]+)\s\]\[TID:(\d+)]\s\[(\d+)\]\s\|\s\s\|\sFile:\s(.+)\s\|\sLine:\s(\d+)\s\|\sFunction:\s(.+)\s\|\s\s\|\sMessage:\s(.+)\s\|\sName:\s(.+)\s\|\sDate:\s(\d+)[\/-](\d+)[\/-](\d+).*", line)
                    if matched is None:
                        continue
                    result_item.error_info = TestCaseRunningError(
                        name=matched.group(1),
                        task_id=int(matched.group(2)),
                        filename=matched.group(4),
                        line_number=int(matched.group(5)),
                        function=matched.group(6),
                        message=matched.group(7),
                        author=matched.group(8),
                        date=datetime.date(int(matched.group(9)), int(matched.group(10)), int(matched.group(11)))
                    )


def get_total_result_html_filename(test_dir: str) -> str:
    return os.path.join(test_dir, __TOTAL_RESULT_FILENAME)


def get_error_test_collection_ini_filename(test_dir: str) -> str:
    return os.path.join(test_dir, __ERROR_TEST_COLLECTION_FILENAME)


def is_test_output_directory(test_dir: str) -> bool:
    if not os.path.isdir(test_dir):
        return False
    ini = get_error_test_collection_ini_filename(test_dir)
    if not os.path.isfile(ini):
        return False
    html = get_total_result_html_filename(test_dir)
    return os.path.isfile(html)


def is_expected_file(filename: str, expected_filename: str, ignore_case: Optional[bool] = False,
                     must_exist: Optional[bool] = True) -> bool:
    if not isinstance(filename, str):
        return False
    if must_exist and not os.path.isfile(filename):
        return False
    directory, basename = os.path.split(filename)
    if ignore_case:
        basename = basename.lower()
        expected_filename = expected_filename.lower()
    return basename == expected_filename


def is_total_result_html_file(filename: str) -> bool:
    return is_expected_file(filename, __TOTAL_RESULT_FILENAME, ignore_case=False, must_exist=True)


def is_error_test_collection_ini_file(filename: str) -> bool:
    return is_expected_file(filename, __ERROR_TEST_COLLECTION_FILENAME, ignore_case=False, must_exist=True)


def parse_total_result_html_file(filename: str, result: TestCaseRunningResultCollection) -> None:
    if not is_total_result_html_file(filename):
        return
    with open(filename, "r", encoding="utf-8") as fp:
        lines: list[str] = fp.readlines()
        for line in lines:
            matched = re.match(__PAT_TOTAL_RESULT_P, line)
            if matched is not None:
                content = matched.group(2)

                # passed
                matched = re.match(__PAT_TOTAL_RESULT_PASSED, content)
                if matched is not None:
                    status = matched.group(1)
                    group, name = matched.group(2).split("\\")
                    cost_seconds = matched.group(3)
                    item = TestCaseRunningResult(
                        status=status,
                        cost_seconds=float(cost_seconds),
                        test_case=TestCase(
                            group=group,
                            name=name
                        )
                    )
                    result.add_item(item)
                    continue

                # failed
                matched = re.match(__PAT_TOTAL_RESULT_ERROR, content)
                if matched is not None:
                    status = matched.group(1)
                    folder = matched.group(2)
                    group, name = matched.group(3).split("\\")
                    cost_seconds = matched.group(4)
                    item = TestCaseRunningResult(
                        status=status,
                        output_directory=folder,
                        cost_seconds=float(cost_seconds),
                        test_case=TestCase(
                            group=group,
                            name=name
                        )
                    )
                    result.add_item(item)
                    continue


def parse_error_test_collection_ini_file(filename: str, result: TestCaseRunningResultCollection) -> None:
    if not is_error_test_collection_ini_file(filename):
        return
    config = configparser.ConfigParser()
    config.read(filename, encoding="utf-8")
    for test_name in config:
        if "\\" not in test_name:
            continue
        group, name = test_name.split("\\")
        result_item = result.get_item_by_name(name)
        if result_item is None:
            continue
        test_case = result_item.test_case
        if test_case is None:
            continue
        test_data = config[test_name]
        for attr_name in test_data:
            attr_value = test_data[attr_name]

            if attr_name == u"runtimelimited":
                test_case.run_time_limited = int(attr_value)
            elif attr_name == u"runspeed":
                test_case.run_speed = int(attr_value)
            elif attr_name == u"count":
                test_case.count = int(attr_value)
            elif attr_name == u"debugmode":
                if attr_value.endswith(u";"):
                    test_case.debug_mode = attr_value[:-1]
                else:
                    test_case.debug_mode = attr_value
            elif attr_name == u"jsfiles":
                if attr_value.endswith(u";"):
                    test_case.js_filename = attr_value[:-1]
                else:
                    test_case.js_filename = attr_value
            elif attr_name == u"isneedtorun":
                test_case.to_run = (attr_value != "0")
            elif attr_name == u"runtype":
                test_case.run_type = attr_value
            elif attr_name == u"exename":
                test_case.exe_name = attr_value
            elif attr_name == u"isdependsource":
                test_case.depend_on_source = (attr_value != "0")


def parse_test_results(test_output_dir: str) -> TestCaseRunningResultCollection:
    result = TestCaseRunningResultCollection()
    if not is_test_output_directory(test_output_dir):
        return result
    html = get_total_result_html_filename(test_output_dir)
    parse_total_result_html_file(html, result)
    ini = get_error_test_collection_ini_filename(test_output_dir)
    parse_error_test_collection_ini_file(ini, result)
    children = os.listdir(test_output_dir)
    for child in children:
        if child == "." or child == "..":
            continue
        path = os.path.join(test_output_dir, child)
        if not os.path.isdir(path):
            continue
        parse_test_result(path, result)
    result.output_directory = test_output_dir
    result.ini_filename = ini
    result.html_filename = html
    return result
