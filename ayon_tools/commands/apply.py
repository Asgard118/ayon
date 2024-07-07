import logging

from ayon_tools.api.attributes import merge_attributes
from ayon_tools.exceptipns import RepositoryDataError, ServerDataError
from ayon_tools.studio import StudioSettings
from ayon_tools import tools


def run(studio: StudioSettings, projects: list[str] = None, **kwargs):
    if isinstance(studio, str):
        studio = StudioSettings(studio)
    fake_apply = kwargs.get("fake")
    # COLLECT DATA
    # collect anatomy

    repo_studio_anatomy = studio.get_rep_anatomy()
    if not repo_studio_anatomy:
        logging.warning("Repository anatomy data is not exists")
    else:
        server_studio_anatomy = studio.get_default_anatomy_preset()
        if not server_studio_anatomy:
            raise ServerDataError("Server anatomy data query failed")
        if not tools.compare_dicts(repo_studio_anatomy, server_studio_anatomy):
            logging.info("Anatomy is missmatch")
            preset_name = studio.get_default_anatomy_preset_name()
            logging.info(f"Apply actual anatomy to {studio}")
            if not fake_apply:
                studio.update_anatomy_preset(preset_name, repo_studio_anatomy)
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
        if not tools.compare_dicts(
            repo_attributes, server_attributes, ignore_keys=["position"]
        ):
            merged_attributes = merge_attributes(server_attributes, repo_attributes)
            logging.info("Attributes is missmatch")
            if not fake_apply:
                studio.set_all_attributes(merged_attributes)
            logging.info("Attributes was applied")
        else:
            logging.info("Attributes is match")
    return
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
