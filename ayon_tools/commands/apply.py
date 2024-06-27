from ayon_tools.studio import StudioSettings
from ayon_tools import tools
import json


def run(studio: StudioSettings, project: list[str] = None, **kwargs):
    # CHECK DIFF
    # projects = project or studio.get_all_projects()

    # apply anatomy
    repo_anatomy = studio.get_rep_anatomy()
    server_anatomy = studio.get_anatomy()
    preset_name = studio.get_default_anatomy_name()
    if not tools.compare_dicts(repo_anatomy, server_anatomy):
        studio.set_anatomy(preset_name, repo_anatomy)


    # apply attributes
    repo_attributes = studio.get_rep_attributes()
    server_attributes = studio.get_attributes()
    if not tools.compare_dicts(repo_attributes, server_attributes):
        for attribute in repo_attributes["attributes"]:
            name_attributes = attribute["name"]
            data_conf = {
                "position": attribute["position"],
                "scope": attribute["scope"],
                "builtin": attribute["builtin"],
                "data": attribute["data"]
            }
            studio.set_attributes(name_attributes, data_conf)


    # apply bundle
    repo_bundle = studio.get_rep_bundle()
    product_bundles_name = studio.get_productions_bundle()
    studio_setting_bundle = studio.get_bundles()
    target_name = product_bundles_name["bundleName"]
    server_bundle = next(
        (
            bundle
            for bundle in studio_setting_bundle.get("bundles", [])
            if bundle.get("name") == target_name
        ),
        None,
    )
    if not tools.compare_dicts(repo_bundle, server_bundle):
        studio.update_bundle(repo_bundle, target_name)


    # appy studio settings

    # apply projects settings
    # for project in projects:
    #     anatomy = studio.get_actual_anatomy(project)
    #     studio.set_project_anatomy(project, anatomy)
    #     studio.set_project_addon_settings(...)
    # CHECK DIFF
