import logging

from ayon_tools.studio import StudioSettings
from ayon_tools import tools


def run(studio: StudioSettings, projects: list[str] = None, **kwargs):
    if isinstance(studio, str):
        studio = StudioSettings(studio)
    # COLLECT DATA

    # apply anatomy
    # if kwargs.get('anatomy', True):
    repo_anatomy = studio.get_rep_anatomy()
    if not repo_anatomy:
        raise Exception('Wrong repository anatomy data')

    server_anatomy = studio.get_anatomy()
    if not server_anatomy:
        raise Exception('Wrong server anatomy data')

    preset_name = studio.get_default_anatomy_name()
    logging.info('Default preset name: %s', preset_name)

    if not tools.compare_dicts(repo_anatomy, server_anatomy):
        studio.set_anatomy(preset_name, repo_anatomy)

    # COMPARE

    # APPLY DIFFS or SHOW DIFFS

    # apply attributes
    repo_attributes = studio.get_rep_attributes()
    if not repo_attributes:
        raise Exception('Wrong repository attributes data')

    server_attributes = studio.get_attributes()
    if not server_attributes:
        raise Exception('Wrong server attributes data')

    # if not tools.compare_dicts(repo_attributes, server_attributes):
    #     for attribute in repo_attributes["attributes"]:
    #         name_attributes = attribute["name"]
    #         data_conf = {
    #             "position": attribute["position"],
    #             "scope": attribute["scope"],
    #             "builtin": attribute["builtin"],
    #             "data": attribute["data"],
    #         }
    #         studio.set_attributes(name_attributes, data_conf)

    # apply bundle
    repo_bundle = studio.get_rep_bundle()
    if not repo_bundle:
        raise Exception('Wrong repository bundle data')

    if kwargs.get("stage"):
        bundle_name = "staging"
        server_bundle = studio.get_productions_bundle()

    else:
        bundle_name = "production"
        server_bundle = studio.get_staging_bundle()

    if not server_bundle:
        installer_version = "1.0.2"  # TODO get from configs
        studio.create_bundle(bundle_name, repo_bundle, installer_version)
        logging.info('Create bundle: %s', bundle_name)

    # else:
    #     if not tools.compare_dicts(repo_bundle, server_bundle):
    #         return studio.update_bundle(server_bundle, repo_bundle)

    # appy studio settings

    repo_addons = studio.get_rep_addons_settings()
    if not repo_addons:
        raise Exception('Wrong repository bundle data')
    print(repo_addons)
    return


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
                studio.set_project_addon_settings(
                    project, addon_name, version, settings
                )
    # CHECK DIFF
