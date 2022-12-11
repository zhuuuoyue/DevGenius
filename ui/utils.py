# coding: utf-8

from typing import Optional

from concepts import CompilationConfiguration


def get_configuration_name(config: CompilationConfiguration) -> Optional[str]:
    if config == CompilationConfiguration.Debug:
        return u"Debug"
    elif config == CompilationConfiguration.Release:
        return u"Release"
    elif config == CompilationConfiguration.QDebug:
        return u"QDebug"
    return None
