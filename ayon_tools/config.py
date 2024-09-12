import os
from pathlib import Path
import json

from ayon_tools.exceptipns import ConfigError

WORKDIR = (
    Path(os.getenv("AYON_TOOLS_WORKDIR") or "~/.ayon_tools").expanduser().resolve()
)
config_file = WORKDIR / "config.json"
TEMPDIR = WORKDIR / "tmp"
TEMPDIR.mkdir(parents=True, exist_ok=True)


def load_config():
    if config_file.exists():
        with config_file.open("r") as stream:
            try:
                return json.load(stream)
            except json.JSONDecodeError:
                raise ConfigError(f"Invalid config file {config_file}")
    raise LookupError(f'App config not found "{config_file}"')


conf = load_config()
REPOSITORY_DIR = WORKDIR / "repository"
DEP_PACKAGES_DIR = WORKDIR / "dep_packages"
INSTALLERS_DIR = WORKDIR / "installers"
REPOSITORY_URL = conf.get("configs_repository_url")
REMOTE_STORAGE_URL = conf.get("remote_storage_url") or "todo..."
BACKEND_URL = (
    conf.get("ayon_backend_repository_url") or "https://github.com/ynput/ayon-backend"
)
STUDIO_CONFIG_DIR = Path(conf.get("studio_config_files_dir") or WORKDIR / "studios")

assert REPOSITORY_URL, f"Repository URL not found in config {config_file}"
assert BACKEND_URL, f"Backend URL not found in config {config_file}"

# ssh
PRIVATE_KEY_PATH = conf.get("private_key_path") or "~/.ssh/id_rsa"
PUBLIC_KEY_PATH = conf.get("public_key_path") or "~/.ssh/id_rsa.pub"


def get_studio_local_config(studio_name):
    config_file = STUDIO_CONFIG_DIR / f"{studio_name}.json"
    if config_file.exists():
        with config_file.open("r") as stream:
            return json.load(stream)
    raise LookupError(f"Studio config not found: {studio_name}")
