# coding: utf-8

import os
import re
from typing import Union


from concepts.test import TestCase, DbgWarnInfo


def analysis_test_result(directory: str) -> Union[TestCase, None]:
    if not os.path.isdir(directory):
        return None
    items = os.listdir(directory)
    for item in items:
        if item.endswith(".js") and not item.endswith("_full.js"):
            path = os.path.join(directory, item)
            with open(path, "r", encoding="utf-8") as fp:
                lines = fp.readlines()
                for line in lines:
                    matched = re.match(r"^\/\/\[([a-zA-Z0-9_]+)\s\]\[TID:(\d+)]\s\[(\d+)\]\s\|\s\s\|\sFile:\s(.+)\s\|\sLine:\s(\d+)\s\|\sFunction:\s(.+)\s\|\s\s\|\sMessage:\s(.+)\s\|\sName:\s(.+)\s\|\sDate:\s(\d+)\/(\d+)\/(\d+).*", line)
                    if matched is None:
                        continue
                    error_type = matched.group(1)
                    if error_type == u"DBG_WARN":
                        error_info = DbgWarnInfo(
                            task_id=int(matched.group(2)),
                            filename=matched.group(4),
                            line_number=int(matched.group(5)),
                            function=matched.group(6),
                            message=matched.group(7),
                            author=matched.group(8)
                        )
                        return TestCase(
                            name=os.path.basename(directory),
                            js_filename=item,
                            error=error_info
                        )


def analysis_test_results(directory: str) -> list[TestCase]:
    if not os.path.isdir(directory):
        return []
    children = os.listdir(directory)
    result: list[TestCase] = []
    for child in children:
        if child == "." or child == "..":
            continue
        path = os.path.join(directory, child)
        case = analysis_test_result(path)
        if case is not None:
            result.append(case)
    return result
