# coding: utf-8

from typing import Optional

from concepts import EnvironmentType


def get_environment_type(path: str) -> Optional[EnvironmentType]:
    """Get EnvironmentManagement name of specified software path.

    Args:
        path: Software path.

    Returns:
        Environment name, for instance EnvironmentType.QA
    """
    return


def switch_environment_type(path: str, env: EnvironmentType) -> None:
    """Switch EnvironmentManagement type of specified software build.

    Args:
        path: Software path.
        env: Target EnvironmentManagement type.

    Returns:
        None.
    """
    return
