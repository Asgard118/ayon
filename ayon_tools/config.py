import os
from pathlib import Path
import json


WORKDIR = (
    Path(os.getenv("AYON_TOOLS_WORKDIR") or "~/.ayon_tools").expanduser().resolve()
)
config_file = WORKDIR / "config.json"
TEMPDIR = WORKDIR / "tmp"
TEMPDIR.mkdir(parents=True, exist_ok=True)


def load_config():
    if config_file.exists():
        with config_file.open("r") as stream:
            return json.load(stream)
    raise LookupError(f'App config not found "{config_file}"')


conf = load_config()
REPOSITORY_DIR = WORKDIR / "repository"
REPOSITORY_URL = conf.get("configs_repository_url")
BACKEND_URL = conf.get("ayon_backend_repository_url")
STUDIO_CONFIG_DIR = Path(conf.get("studio_config_files_dir") or WORKDIR / "studios")

assert REPOSITORY_URL, f"Repository URL not found in config {config_file}"
assert BACKEND_URL, f"Backend URL not found in config {config_file}"


def get_studio_local_config(studio_name):
    config_file = STUDIO_CONFIG_DIR / f"{studio_name}.json"
    if config_file.exists():
        with config_file.open("r") as stream:
            return json.load(stream)
    raise LookupError(f"Studio config not found: {studio_name}")
