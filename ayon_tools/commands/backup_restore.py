import json
import logging
import tempfile

from ayon_tools.studio import StudioSettings
from pathlib import Path


def dump(studio: StudioSettings, path: str = None, **kwargs):
    if isinstance(studio, str):
        studio = StudioSettings(studio, **kwargs)

    path = Path(path or tempfile.mktemp(suffix=".json"))
    path.parent.mkdir(parents=True, exist_ok=True)
    # studio data
    data = dict(
        server_anatomy=studio.get_default_anatomy_preset(),
        server_attributes=studio.get_attributes(),
        server_staging_bundle=studio.get_staging_bundle(),
        server_production_bundle=studio.get_productions_bundle(),
        server_addons=studio.get_server_addons_settings(),
        projects={},
    )
    # projects data
    projects = studio.get_projects()
    for project in projects:
        data["projects"][project["name"]] = dict(
            anatomy=studio.get_project_anatomy(project["name"]),
            settings=studio.get_project_addons_settings(project["name"]),
            projects_settings_staging=studio.get_project_settings_for_status("staging", project["name"]),
            projects_settings_production=studio.get_project_settings_for_status("production", project["name"])
        )
    with open(path, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return path.as_posix()


def restore(studio: StudioSettings, path: str, **kwargs):
    if isinstance(studio, str):
        studio = StudioSettings(studio, **kwargs)
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Path '{path}' does not exist.")
    with path.open() as file:
        data = json.load(file)

    # studio anatomy
    preset_name = studio.get_default_anatomy_preset_name()
    studio.update_anatomy_preset(preset_name, data["server_anatomy"])

    # attributes
    attributes = data["server_attributes"]
    for attribute in attributes["attributes"]:
        name = attribute["name"]
        setting = attribute["data"]
        scope = attribute["scope"]
        studio.set_attributes_config(attribute_name=name, data=setting, scope=scope)

    # bundle
    studio.update_bundle("staging", data["server_staging_bundle"])
    studio.update_bundle("production", data["server_production_bundle"])

    # addons
    for addon_name, addon_ver in data["server_production_bundle"]["addons"].items():
        settings = data["server_addons"].get(addon_name, {})
        if addon_name == "ayon_ocio":
            continue
        studio.set_addon_settings(addon_name, addon_ver, settings)

    # project
    if data.get("projects"):
        for project_name, project_data in data["projects"].items():
            logging.info(f"Apply project {project_name}")
            # project anatomy
            studio.set_project_anatomy(project_name, project_data["anatomy"])

            # project productions settings
            for addons in project_data["settings"].items():
                addon_name, settings = addons
                for addon in project_data["projects_settings_production"]["addons"]:
                    if addon_name == "ayon_ocio":
                        continue
                    if addon["name"] == addon_name:
                        version = addon["version"]
                        studio.set_project_addon_settings(project_name, addon_name, version, settings)

            # project staging settings
            for addons in project_data["settings"].items():
                addon_name, settings = addons
                for addon in project_data["projects_settings_staging"]["addons"]:
                    if addon_name == "ayon_ocio":
                        continue
                    if addon["name"] == addon_name:
                        version = addon["version"]
                        studio.set_project_addon_settings(project_name, addon_name, version, settings)