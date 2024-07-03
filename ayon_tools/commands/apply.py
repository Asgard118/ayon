import logging

from ayon_tools.exceptipns import RepositoryDataError, ServerDataError
from ayon_tools.studio import StudioSettings
from ayon_tools import tools


def run(studio: StudioSettings, projects: list[str] = None, **kwargs):
    if isinstance(studio, str):
        studio = StudioSettings(studio)

    # COLLECT DATA
    # collect anatomy
    repo_anatomy = studio.get_rep_anatomy()
    if not repo_anatomy:
        logging.warning("Repository anatomy data is not exists")
    else:
        server_anatomy = studio.get_anatomy()
        if not server_anatomy:
            raise ServerDataError("Server anatomy data query failed")
        preset_name = studio.get_default_anatomy_preset_name(studio.default_settings, repo_anatomy)
        studio.set_primary(preset_name)
        logging.info("Default preset name: %s", preset_name)
        return
        if not tools.compare_dicts(server_anatomy, repo_anatomy):
            logging.info("Anatomy is missmatch")
            studio.set_anatomy_preset(preset_name, repo_anatomy)
        else:
            logging.info("Anatomy is OK")




    # collect attributes
    repo_attributes = studio.get_rep_attributes()
    if not repo_attributes:
        logging.warning("Repository attributes data is not exists")
    else:
        server_attributes = studio.get_attributes()
        if not server_attributes:
            raise ServerDataError("Wrong server attributes data")
        if not tools.compare_dicts(repo_attributes, server_attributes):
            if not tools.compare_dicts_diff(repo_attributes, server_attributes):
                logging.info("Attributes is missmatch")
                studio.set_attributes(repo_attributes)
                # for attribute in repo_attributes["attributes"]:
                #     name_attributes = attribute["name"]
                #     data_conf = {
                #         "position": attribute["position"],
                #         "scope": attribute["scope"],
                #         "builtin": attribute["builtin"],
                #         "data": attribute["data"],
                #     }
                #     studio.set_attributes(name_attributes, data_conf)
            else:
                logging.info("Attributes is OK")

    # collect bundle
    is_staging = bool(kwargs.get("stage"))
    bundle_name = "staging" if is_staging else "production"
    repo_bundle = studio.get_rep_bundle()
    if not repo_bundle:
        logging.warning("Repository bundle data is not exists")
    else:
        if is_staging:
            server_bundle = studio.get_staging_bundle()
        else:
            server_bundle = studio.get_productions_bundle()
        repo_bundle["isProduction"] = not is_staging
        repo_bundle["isStaging"] = is_staging
        if not server_bundle:
            logging.info("Create bundle: %s", bundle_name)
            studio.create_bundle(bundle_name, repo_bundle)
        else:
            logging.info("Update bundle %s", bundle_name)
            studio.update_bundle(bundle_name, repo_bundle)

    # collect addons
    if repo_bundle:
        # здесь мы уже уверены что состав бандла и версии аддонов соответствует
        server_addons = studio.get_addons()
        if not server_addons:
            raise ServerDataError("Wrong server addon data")
        for addon_name, version in repo_bundle["addons"].items():
            if addon_name not in server_addons:
                raise RepositoryDataError(
                    f"Addon {addon_name} not found in server data"
                )
            repo_addon_settings = studio.get_rep_addon_settings(addon_name)
            if not repo_addon_settings:
                continue
            studio_addon_settings = studio.get_addon_settings(addon_name, version)
            if tools.compare_dicts(repo_addon_settings, studio_addon_settings):
                continue
            studio.set_addon_settings(addon_name, version, repo_addon_settings)

    return
    projects = projects or studio.get_projects()

    # apply projects settings
    if projects:
        for project in projects:
            anatomy = studio.get_rep_anatomy(project)
            if not anatomy:
                raise Exception("Wrong anatomy data")

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
