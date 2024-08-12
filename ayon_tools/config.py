import os
from pathlib import Path
import json


WORKDIR = (
    Path(os.getenv("AYON_TOOLS_WORKDIR") or "~/.ayon_tools").expanduser().resolve()
)


def load_config():
    config_file = WORKDIR / "config.json"
    if config_file.exists():
        with config_file.open("r") as stream:
            return json.load(stream)
    raise LookupError(f'App config not found "{config_file}"')


conf = load_config()
REPOSITORY_DIR = WORKDIR / "repository"
REPOSITORY_URL = conf.get("configs_repository_url")
BACKEND_URL = conf.get("ayon_backend_repository_url")
STUDIO_CONFIG_DIR = Path(conf.get("studio_config_files_dir") or WORKDIR / "studios")


def get_studio_local_config(studio_name):
    config_file = STUDIO_CONFIG_DIR / f"{studio_name}.json"
    if config_file.exists():
        with config_file.open("r") as stream:
            return json.load(stream)
    raise LookupError(f"Studio config not found: {studio_name}")
