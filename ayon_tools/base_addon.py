import json
from pathlib import Path

from ayon_tools.repository import repo


class Addon:
    def __init__(self, name):
        self.name = name

    @classmethod
    def get(cls, name: str, studio_name: str): ...

    def get_default_settings(self, studio_name: str):
        default_settings_path = Path("addons", self.name, "defaults.json").as_posix()
        return repo.get_file_content(default_settings_path, studio_name)

    def get_settings(self, studio_name: str = None, project: str = None):
        # get default
        settings = self.get_default_settings(studio_name)
        # resolve shortcuts
        settings = self.solve_shortcuts(settings, project)
        return settings

    def build(self) -> str: ...

    def solve_shortcuts(self, settings: dict, project: str = None):
        # TODO: apply shortcuts
        # TODO: apply project shortcuts
        return settings

    def get_custom_attributes(self):
        pass