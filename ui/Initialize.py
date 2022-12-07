# coding: utf-8

from .command import get_command_manager

from .RepositoryManagement.RepositoryManagementCommand import RepositoryManagementCommand
from .Tasks import TaskManagementCommand
from .Packaging import PackagingCommand
from .ArchiveManagement import ArchiveManagementCommand
from .CreateFiles import CreateFilesCommand
from .EnvironmentManagement import SwitchEnvironmentCommand
from .Preferences import PreferencesCommand
from .About import AboutCommand


def initialize_commands():
    cmd_mgr = get_command_manager()
    cmd_mgr.register("project", RepositoryManagementCommand)
    cmd_mgr.register("task", TaskManagementCommand)
    cmd_mgr.register("packaging", PackagingCommand)
    cmd_mgr.register("archive", ArchiveManagementCommand)
    cmd_mgr.register("create_files", CreateFilesCommand)
    cmd_mgr.register("environment", SwitchEnvironmentCommand)
    cmd_mgr.register("preferences", PreferencesCommand)
    cmd_mgr.register("about", AboutCommand)


def initialize():
    initialize_commands()
