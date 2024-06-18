import os
from pathlib import Path
import json
from .api.auth import default_auth

WORKDIR = Path(os.getenv("AYON_TOOLS_WORKDIR") or '~/.ayon_tools').expanduser()


def load_config():
    config_file = WORKDIR / "config.json"
    if config_file.exists():
        with config_file.open("r") as stream:
            return json.load(stream)
    return dict()


conf = load_config()
REPOSITORY_DIR = WORKDIR / "repository"
REPOSITORY_URL = conf.get("configs_repository_url")
STUDIO_CONFIG_DIR = WORKDIR / "studios"

class StudioData():
    def __int__(self, auth):
        self.auth = auth

    def get_addons_data(self):
        ...

    def get_addon_data(self):
        ...

    def get_anatomy_data(self):
        ...

    def get_attributes_data(self):
        ...

    def get_bundle_data(self):
        ...

    def get_studio_data(self):
        ...

    def get_project_data(self, project_name):
        ...