import json

from ayon_tools.studio import StudioSettings

def save_data_to_json_file(data_dict: dict, filename: str):
    try:
        with open(filename, 'r') as f:
            file_data = json.load(f)
    except FileNotFoundError:
        file_data = {}
    file_data.update(data_dict)
    with open(filename, 'w') as f:
        json.dump(file_data, f, indent=4, ensure_ascii=False)

def dump(studio: StudioSettings, path: str):
    server_anatomy = studio.get_default_anatomy_preset()
    server_attributes = studio.get_attributes()
    server_staging_bundle = studio.get_staging_bundle()
    server_production_bundle = studio.get_productions_bundle()
    server_addons = studio.get_server_addons_settings()
    projects = studio.get_projects()
    for project in projects:
        server_anatomy_project = studio.get_project_anatomy(project['name'])
        save_data_to_json_file(
            {f"project_{project['name']}_anatomy": server_anatomy_project},
            path
        )
        server_addon_project = studio.get_project_addons_settings(project['name'])
        save_data_to_json_file(
            {f"project_{project['name']}_addons": server_addon_project},
            path
        )
    save_data_to_json_file(
        {
            "addons": server_addons,
            "server_production_bundle": server_production_bundle,
            "server_staging_bundle": server_staging_bundle,
            "attributes": server_attributes,
            "anatomy": server_anatomy,
        },
        path
    )
    return path

def restore(studio: StudioSettings, data: dict):
    #anatomy
    preset_name = studio.get_default_anatomy_preset_name()
    studio.update_anatomy_preset(preset_name, data["anatomy"])