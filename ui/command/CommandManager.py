# coding: utf-8

from typing import Dict

from .ICommand import ICommand


class CommandCreator(object):

    def __init__(self, command):
        self.command = command

    def create(self) -> ICommand:
        return self.command()


class CommandManager(object):

    def __init__(self):
        self.commands: Dict[str, CommandCreator] = {}

    def register(self, name: str, command):
        self.commands[name] = CommandCreator(command)

    def run(self, name: str) -> None:
        if name in self.commands:
            self.commands[name].create().execute()


_command_manager = CommandManager()


def get_command_manager():
    return _command_manager
