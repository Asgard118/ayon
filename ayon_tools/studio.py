import logging

from . import api
from . import config
from .repository import repo


class StudioSettings:
    bundle_config_file = "defaults/bundle.json"
    anatomy_config_file = "defaults/anatomy.json"
    attributes_config_file = "defaults/attributes.json"
    studio_config_file = "addons/{addon_name}/defaults.json"
    project_settings_file = "projects/{project}/project_settings.json"
    project_anatomy_file = "projects/{project}/project_anatomy.json"
    default_settings = "default"

    def __init__(self, name: str):
        self.name = name
        studio_config = self.get_config_data()
        self.auth = api.auth.Auth(**studio_config)

    def get_rep_pop(self):
        pass

    def get_projects(self) -> list:
        return []

    def get_config_data(self):
        studio_local_config = config.get_studio_local_config(self.name)
        if (
            "server_url" not in studio_local_config
            or "token" not in studio_local_config
        ):
            raise ValueError("Invalid config file")
        return studio_local_config

    # studio configs
    def get_addon_settings(self, name: str, ver: str):
        return api.addons.get_addon_studio_settings(name, ver, auth=self.auth)

    def get_addons(self):
        return api.addons.get_studio_settings(auth=self.auth)

    def set_addon_settings(self, name: str, ver: str, settings: dict):
        api.addons.set_studio_settings(name, ver, settings)

    def get_anatomy(self, preset_name: str = None):
        return api.anatomy.get_studio_anatomy_preset(preset_name, auth=self.auth)

    def set_primary(self, preset_name: str):
        return api.anatomy.set_primary_preset(preset_name, auth=self.auth)

    def create_anatomy(self, preset_name: str, preset: dict):
        return api.anatomy.create_studio_anatomy_preset(preset_name, preset, auth=self.auth)

    def get_attributes(self):
        return api.attributes.get_attributes(auth=self.auth)

    def set_attributes(self, attributes: dict):
        for attr, data in attributes.items():
            api.attributes.set_attributes(attr, data, auth=self.auth)

    def get_bundle(self, bundle_name: str):
        return api.bundles.get_bundle(bundle_name, auth=self.auth)

    def get_bundles(self):
        return api.bundles.get_bundles(auth=self.auth)

    def update_bundle(self, bundle_name: str, settings: dict):
        return api.bundles.update_bundle(bundle_name, settings, auth=self.auth)

    def get_productions_bundle(self):
        return api.bundles.get_production_bundle(auth=self.auth)

    def get_staging_bundle(self):
        return api.bundles.get_staging_bundle(auth=self.auth)

    def create_bundle(self, name: str, data: dict):
        installer_version: str = data["installer_version"]
        addon_list = data["addons"]
        return api.bundles.create_bundle(
            name, addon_list, installer_version, auth=self.auth
        )

    # project configs
    def get_project_anatomy(self, project_name: str):
        return api.anatomy.get_project_anatomy(project_name, auth=self.auth)

    def set_project_anatomy(self, project_name: str, settings: dict):
        return api.anatomy.set_project_anatomy(project_name, settings, auth=self.auth)

    def get_project_addons_settings(self, project_name: str):
        return api.addons.get_project_settings(project_name, auth=self.auth)

    def set_project_addon_settings(
        self, project_name: str, addon_name: str, addon_version: str, settings: dict
    ):
        return api.addons.set_project_settings(
            addon_name, addon_version, project_name, settings, auth=self.auth
        )

    def set_anatomy_preset(self, preset_name: str, preset: dict):
        return api.anatomy.set_studio_anatomy_preset(
            preset_name, preset, auth=self.auth
        )

    def get_anatomy_presets(self):
        return api.anatomy.get_studio_anatomy_presets_names(auth=self.auth)

    def get_default_anatomy_preset_name(self, compare_name: str, rep_preset: dict):
        return api.anatomy.get_anatomy_name(compare_name, rep_preset, auth=self.auth)

    def update_project(self, *args, **kwargs):
        return api.addons.update_project(auth=self.auth, *args, **kwargs)

    # studio from repo
    def get_rep_bundle(self):
        """
        Актуальный состав бандла из репозитория
        """
        bundle = repo.get_file_content(self.bundle_config_file, self.name)
        return bundle

    def get_rep_addon_settings(self, addon_name: str, project: str = None):
        """
        Актуальные студийные настройки аддона из репозитория
        """
        addons = repo.get_file_content(
            self.studio_config_file.format(addon_name=addon_name), self.name
        )
        if project:
            from . import tools

            try:
                project_addons = repo.get_file_content(
                    self.project_settings_file.format(project=project), self.name
                )
            except FileNotFoundError:
                logging.debug("No project overrides")
            else:
                tools.update_dict_with_changes(addons, project_addons)
        return addons

    def get_rep_anatomy(self, project: str = None):
        """
        Актуальный пресет анатомии из репозитория
        """
        anatomy = repo.get_file_content(self.anatomy_config_file, self.name)
        if project:
            from . import tools

            project_anatomy = repo.get_file_content(
                self.project_anatomy_file.format(project=project), self.name
            )
            if not tools.compare_dicts(anatomy, project_anatomy):
                tools.update_dict_with_changes(anatomy, project_anatomy)
        return anatomy

    def get_rep_attributes(self):
        """
        Актуальные студийные атрибуты из репозитория
        """
        attributes = repo.get_file_content(self.attributes_config_file, self.name)
        # iterate addons
        return attributes

    # project from repo
    def get_rep_project_anatomy(self, project_name: str):
        """
        Актуальная анатомия проекта
        """
        # TODO

    def get_rep_project_addons(self):
        """
        Настройки всех аддонов проекта.
        Структура настроек должна подходить под указанные в бандле версии
        """
        # TODO

    # utils
