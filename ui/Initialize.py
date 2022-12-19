# coding: utf-8

from .command import get_command_manager

from .RepositoryManagement.RepositoryManagementCommand import RepositoryManagementCommand
from .Tasks import TaskManagementCommand
from .Packaging import PackagingCommand
from .ArchiveManagement import ArchiveManagementCommand
from .CreateFiles import CreateFilesCommand
from .EnvironmentManagement import SwitchEnvironmentCommand
from .test import AnalysisTestResultCommand
from .setting import SettingCommand
from .About import AboutCommand
from .other import AlwaysOnTopCommand


def initialize_commands():
    cmd_mgr = get_command_manager()
    cmd_mgr.register("project", RepositoryManagementCommand)
    cmd_mgr.register("task", TaskManagementCommand)
    cmd_mgr.register("packaging", PackagingCommand)
    cmd_mgr.register("archive", ArchiveManagementCommand)
    cmd_mgr.register("create_files", CreateFilesCommand)
    cmd_mgr.register("environment", SwitchEnvironmentCommand)
    cmd_mgr.register("analysis_test_result", AnalysisTestResultCommand)
    cmd_mgr.register("preferences", SettingCommand)
    cmd_mgr.register("about", AboutCommand)
    cmd_mgr.register("always_on_top", AlwaysOnTopCommand)


def initialize():
    initialize_commands()
