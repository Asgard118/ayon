import json
from pathlib import Path

from ayon_tools.repository import repo


class Addon:
    def __init__(self, name):
        self.name = name

    def get_default_settings(self, studio_name: str):
        default_settings_path = Path("addons", self.name, "defaults.json").as_posix()
        return repo.get_file_content(default_settings_path, studio_name)

    def get_settings(self, studio_name: str = None, project: str = None):
        settings = self.get_default_settings(studio_name)
        # TODO: switch to project
        settings = self.solve_shortcuts(settings, project)
        return settings

    def solve_shortcuts(self, settings: dict, project: str = None):
        # TODO: apply shortcuts
        return settings
