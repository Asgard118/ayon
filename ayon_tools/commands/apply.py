from ayon_tools.studio import StudioSettings
from ayon_tools import tools


def run(studio: StudioSettings, projects: list[str] = None, **kwargs):
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
    github_data = studio.get_rep_bundle()
    product_bundles_name = studio.get_productions_bundle()
    studio_setting_bundle = studio.get_bundles()
    target_name = product_bundles_name['bundleName']
    bundles_to_compare = next(
        (
            bundle
            for bundle in studio_setting_bundle.get("bundles", [])
            if bundle.get("name") == target_name
        ),
        None
    )
    if not tools.compare_dicts(github_data, bundles_to_compare):
        return studio.update_bundle(target_name, github_data)


    # appy studio settings
    repo_addons = studio.get_rep_addons_settings()
    server_addons = studio.get_addons()
    bundle_with_addons = studio.get_rep_bundle()
    if not tools.compare_dicts(repo_addons, server_addons):
        for addon_name, settings_dict in repo_addons.items():
            if addon_name in bundle_with_addons["addons"]:
                version = bundle_with_addons["addons"][addon_name]
                settings = settings_dict
                studio.set_addon_settings(addon_name, version, settings)


    # apply projects settings
    for project in projects:
        anatomy = studio.get_rep_anatomy(project)
        settings_project = studio.get_rep_addons_settings(project)
        studio.set_project_anatomy(project, anatomy)
        for addon_name, settings_dict in settings_project.items():
            if addon_name in bundle_with_addons["addons"]:
                version = bundle_with_addons["addons"][addon_name]
                settings = settings_dict
                studio.set_project_addon_settings(project, addon_name, version, settings)
    # CHECK DIFF
