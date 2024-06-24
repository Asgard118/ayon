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
    product_bundles_name = studio.get_productions_bundle()
    studio_setting_bundle = studio.get_bundles()
    target_name = product_bundles_name['bundleName']
    bundles_to_compare = next((bundle for bundle in studio_setting_bundle.get("bundles", []) if bundle.get("name") == target_name), None)
    github_data = fetch_file_contents(config.REPOSITORY_URL, studio.bundle_config_file, config.REPOSITORY_DIR)

    if compare_dicts(github_data, bundles_to_compare):
        return None
    else:
        return studio.update_bundle(github_data, target_name)
