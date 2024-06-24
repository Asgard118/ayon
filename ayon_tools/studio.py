from .api import anatomy, bundles, attributes, auth, addons
from . import config
from .repository import repo


class StudioSettings:
    bundle_config_file = "bundle/bundles_settings.json"

    def __init__(self, name: str):
        self.name = name
        studio_config = self.get_config_data()
        self.auth = auth.Auth(**studio_config)

    def get_config_data(self):
        studio_local_config = config.get_studio_local_config(self.name)
        if (
            "server_url" not in studio_local_config
            or "token" not in studio_local_config
        ):
            raise ValueError("Invalid config file")
        return studio_local_config

    # studio configs

    def get_addon(self, name: str, ver: str):
        return addons.get_addon_studio_settings(name, ver, auth=self.auth)

    def get_anatomy(self, preset_name: str = None):
        return anatomy.get_studio_anatomy_preset(preset_name, auth=self.auth)

    def get_attributes(self):
        return attributes.get_attributes(auth=self.auth)

    def get_bundle(self, bundle_name: str):
        return bundles.get_bundle(bundle_name, auth=self.auth)

    def get_bundles(self):
        return bundles.get_bundles(auth=self.auth)

    def update_bundle(self, bundle_name: str, settings: dict):
        return bundles.update_bundle(bundle_name, settings, auth=self.auth)

    def get_productions_bundle(self):
        return bundles.get_production_bundle(auth=self.auth)

    def get_staging_bundle(self):
        return bundles.get_staging_bundle(auth=self.auth)

    # project configs

    def get_project_anatomy(self, project_name: str):
        return anatomy.get_project_anatomy(project_name, auth=self.auth)

    def set_project_anatomy(self, project_name: str, settings: dict):
        return anatomy.set_project_anatomy(project_name, settings, auth=self.auth)

    def get_project_addons_settings(self, project_name: str):
        return addons.get_project_settings(project_name, auth=self.auth)

    def set_project_addon_settings(
        self, project_name: str, addon_name: str, addon_version: str, settings: dict
    ):
        return addons.set_project_settings(
            addon_name,
            addon_version,
            project_name,
            settings,
            auth=self.auth,
        )

    # studio from repo
    def get_actual_bundle(self):
        """
        Актуальный состав бандла
        """
        return repo.get_file_content(self.name, "bundle/bundle_settings.json")

    def get_actual_addon_settings(self, addon_name: str):
        """
        Актуальные студийные настройки аддона из репозитория
        """
        # TODO

    def get_actual_anatomy(self, project: str = None):
        """
        Актуальный пресет анатомии из репозитория
        """
        # TODO

    def get_actual_attributes(self):
        """
        Актуальные студийные атрибуты из репозитория
        """
        # TODO

    # project from repo
    def get_actual_project_anatomy(self, project_name: str):
        """
        Актуальная анатомия проекта
        """
        # TODO

    def get_actual_project_addons(self):
        """
        Настройки всех аддонов проекта.
        Структура настроек должна подходить под указанные в бандле версии
        """
        # TODO

    # utils
