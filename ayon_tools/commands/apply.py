from ayon_tools.api import bundles, addons
from ayon_tools.studio import Studio
from ayon_tools import config
import pygit2
import json
import requests

def compare_dicts(dict1, dict2):
            return dict1 == dict2

def fetch_file_contents(repo_url, file_path, clone_path):
    pygit2.clone_repository(repo_url, clone_path)
    file_full_path=f"{clone_path}/{file_path}"
    json_data = {}
    with open(file_full_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data


def apply(studio: Studio, project: list[str] = None, *kwargs):
    studio_setting_bundle = bundles.get_production_bundle()
    github_data = fetch_file_contents(config.REPOSITORY_URL, studio.bundle_config_file, config.REPOSITORY_DIR)

    if compare_dicts(github_data, studio_setting_bundle):
        return None
    else:
        for addon in github_data["addons"]:
            addon_name = addon["name"]
            version = addon["version"]
            settings = addon["settings"]

            try:
                addons.set_studio_settings(addon_name, version, settings)
            except requests.HTTPError as e:
                print(f"Ошибка {addon_name} версии {version}: {e}")
