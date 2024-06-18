import os
from pathlib import Path
import json

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

