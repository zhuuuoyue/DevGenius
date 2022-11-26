# coding: utf-8

from .command import get_command_manager

from .ProjectCommand import ProjectCommand


def initialize_commands():
    cmd_mgr = get_command_manager()
    cmd_mgr.register("project", ProjectCommand)


def initialize():
    initialize_commands()
