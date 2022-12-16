# coding: utf-8

from .setting import get_authors


def get_header_content(*arg, **kwargs) -> str:
    authors = get_authors()
    return f"""// Owner: {authors.owner}
// Co-Owner: {authors.co_owner}

#pragma once

namespace gap
{{
}}

"""


def get_source_content(*args, **kwargs) -> str:
    include_header_line = ""
    if "header_filename" in kwargs:
        header_filename = kwargs.pop("header_filename")
        include_header_line = f"""
#include "{header_filename}"
"""
    authors = get_authors()
    return f"""// Owner: {authors.owner}
// Co-Owner: {authors.co_owner}
{include_header_line}
#include "EnableCompileWarning_The_LAST_IncludeInCpp.h"

using namespace gap;

"""
