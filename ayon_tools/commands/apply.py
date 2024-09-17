import json
import logging

from ayon_tools.api.attributes import merge_attributes
from ayon_tools.exceptipns import RepositoryDataError, ServerDataError
from ayon_tools.studio import StudioSettings
from ayon_tools import tools
from ayon_tools.tools import show_dict_diffs
from ayon_tools.api import ayon_tools_addon


def run(
    studio: StudioSettings,
    projects: list[str] = None,
    operations: list = None,
    **kwargs,
):
    if isinstance(studio, str):
        studio = StudioSettings(studio, **kwargs)
    fake_apply = kwargs.get("fake")
    verbose = kwargs.get("verbose", False)
    is_staging = bool(kwargs.get("stage"))
    projects = projects or studio.get_project_names()

    studio.disable_onboarding()
    ayon_tools_addon.ensure_installed(studio)

    # apply anatomy
    if not operations or ("anatomy" in operations):
        logging.info("Apply anatomy...")
        apply_anatomy(studio, projects, fake_apply, verbose)
    else:
        logging.info("Skip anatomy")

    # apply bundle
    if not operations or ("bundle" in operations):
        apply_bundle(studio, is_staging, fake_apply, **kwargs)
    else:
        logging.info("Skip bundle")

    # apply attributes
    if not operations or ("attrs" in operations):
        apply_attributes(studio, fake_apply, verbose)
    else:
        logging.info("Skip attributes")

    logging.info("Apply command finished!")

    # apply settings
    if not operations or ("settings" in operations):
        apply_studio_settings(studio, is_staging, fake_apply, **kwargs)
    else:
        logging.info("Skip settings")
    # per project settings
    # projects = projects or studio.get_project_names()
    # apply projects settings


def apply_bundle(
    studio: StudioSettings,
    is_staging=False,
    fake_apply=False,
    **kwargs,
):
    """
    Создаёт или обновляет бандл
    Билдит и инсталит аддоны отсутствующих версий
    """
    bundle_name = "staging" if is_staging else "production"
    # get or create bundle
    repo_bundle = studio.get_rep_bundle()
    if not repo_bundle:
        logging.warning("Repository bundle data is not exists")
        return
    # check and install addons

    restart_required = False
    for addon_name, addon_version in repo_bundle["addons"].items():
        # get addon class
        # addon = Addon.get_addon_instance(addon_name, studio)
        # check is installed on server
        if not studio.addon_installed(addon_name, addon_version):
            logging.info(f"Install addon {addon_name} {addon_version}")
            studio.install_addon(addon_name, addon_version)
            restart_required = True
        else:
            logging.info(f"Addon {addon_name} {addon_version} already installed")
            # Addon.get_addon_instance(addon_name, studio)
    if restart_required:
        logging.info("Restarting...")
        studio.restart_server()
        logging.info("Continue...")
    if is_staging:
        server_bundle = studio.get_staging_bundle()
    else:
        server_bundle = studio.get_productions_bundle()
    # installers
    studio.add_installer(repo_bundle["installer_version"])
    studio.restart_server()
    # dep packages
    repo_bundle["dependency_packages"] = studio.add_dep_packages(
        repo_bundle["dependency_packages"]
    )
    if not server_bundle:
        # create new bundle
        logging.info("Create bundle: %s", bundle_name)
        if not fake_apply:

            studio.create_bundle(
                bundle_name,
                addons=repo_bundle["addons"],
                installer_version=repo_bundle["installer_version"],
                is_production=not is_staging,
                is_staging=is_staging,
                dependency_packages=repo_bundle["dependency_packages"],
            )
    else:
        # update bundle
        logging.info("Update bundle: %s", bundle_name)
        if not fake_apply:
            studio.restart_server()
            studio.update_bundle(bundle_name, repo_bundle)


def apply_studio_settings(
    studio: StudioSettings,
    is_staging=False,
    fake_apply=False,
    **kwargs,
):
    """
    Назначает настройки на аддоны сервера
    Нужные версии аддонов уже должны быть инсталированны в бандл
    """
    from ayon_tools.api.bundles import BundleVariant

    variant = BundleVariant.STAGING if is_staging else BundleVariant.PRODUCTION

    server_addons = studio.get_server_addons_settings(variant, variant)
    if not server_addons:
        raise ServerDataError("Wrong server addon data")

    repo_bundle = studio.get_rep_bundle()
    for addon_name, version in repo_bundle["addons"].items():
        if addon_name not in server_addons:
            raise RepositoryDataError(f"Addon {addon_name} not found in server data")
        addon = studio.get_addon(addon_name)
        repo_addon_settings = addon.get_repo_settings()
        if not repo_addon_settings:
            logging.debug(f"Empty settings for {addon_name}")
            continue
        if not fake_apply:
            studio.set_addon_settings(addon_name, version, repo_addon_settings)
        else:
            logging.info(f"Fake apply settings for {addon_name}")


def apply_anatomy(
    studio: StudioSettings,
    projects: list,
    fake_apply=False,
    verbose=None,
    **kwargs,
):
    # default anatomy
    repo_studio_anatomy = studio.get_rep_anatomy()
    if not repo_studio_anatomy:
        logging.warning("Repository anatomy data is not exists")
    else:
        server_studio_anatomy = studio.get_default_anatomy_preset()
        if not server_studio_anatomy:
            raise ServerDataError("Server anatomy data query failed")

        if not tools.compare_dicts(repo_studio_anatomy, server_studio_anatomy):
            logging.info("Studio anatomy is missmatch")
            if verbose:
                show_dict_diffs(repo_studio_anatomy, server_studio_anatomy)
            preset_name = studio.get_default_anatomy_preset_name()
            logging.info(
                f"Apply actual studio anatomy preset {preset_name} to {studio}"
            )
            if not fake_apply:
                studio.update_anatomy_preset(preset_name, repo_studio_anatomy)
        else:
            logging.info("Studio Anatomy is OK")

    # projects anatomy
    for project_name in projects:
        logging.info(f"Check anatomy for {project_name}")
        repo_project_anatomy = studio.get_rep_anatomy(project_name)
        server_project_anatomy = studio.get_project_anatomy(project_name)
        if not tools.compare_dicts(repo_project_anatomy, server_project_anatomy):
            logging.info(f"Anatomy is missmatch for {project_name}")
            if not fake_apply:
                studio.set_project_anatomy(project_name, repo_project_anatomy)
                logging.info("Anatomy was applied")


def apply_attributes(studio: StudioSettings, fake_apply=False, verbose=None, **kwargs):
    repo_attributes = studio.get_rep_attributes()
    if not repo_attributes:
        logging.warning("Repository attributes data is not exists")
        return

    server_attributes = studio.get_attributes()
    if not server_attributes:
        raise ServerDataError("Wrong server attributes data")

    if tools.compare_dicts(
        repo_attributes, server_attributes, ignore_keys=["position"]
    ):
        logging.info("Attributes is OK")
        return

    merged_attributes = merge_attributes(server_attributes, repo_attributes)
    logging.info("Attributes is missmatch")
    if not fake_apply:
        for attribute in merged_attributes["attributes"]:
            attribute["attribute_name"] = attribute.pop("name")
            studio.set_attributes_config(**attribute)
        logging.info("Attributes was applied")


# if projects:
#     for project in projects:
#         anatomy = studio.get_rep_anatomy(project)
#         if not anatomy:
#             raise Exception("Wrong anatomy data")
#
#         settings_project = studio.get_rep_addons_settings(project)
#         studio.set_project_anatomy(project, anatomy)
#         for addon_name, settings_dict in settings_project.items():
#             if addon_name in bundle_with_addons["addons"]:
#                 version = bundle_with_addons["addons"][addon_name]
#                 settings = settings_dict
#                 studio.set_project_addon_settings(
#                     project, addon_name, version, settings
#                 )
