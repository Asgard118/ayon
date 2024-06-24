from .api import anatomy, bundles, attributes, auth, addons
from . import config


class Studio:
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

    def get_addons_data(self, project_name: str):
        return addons.get_project_settings(project_name, auth=self.auth)

    def get_addon_data(self, name: str, ver: str):
        return addons.get_addon_studio_settings(name, ver, auth=self.auth)

    def get_anatomy_data(self, preset_name: str):
        return anatomy.get_studio_anatomy_preset(preset_name, auth=self.auth)

    def get_attributes_data(self):
        return attributes.get_attributes(auth=self.auth)

    def get_bundle_data(self, name: str):
        return bundles.get_bundle(name, auth=self.auth)

    def get_bundles(self):
        return bundles.get_bundles(auth=self.auth)

    def get_productions_bundle(self):
        return bundles.get_production_bundle(auth=self.auth)

    def get_project_anatomy_data(self, project_name: str):
        return anatomy.get_project_anatomy(project_name, auth=self.auth)

    def update_bundle(self, settings: dict, bundle_name: str):
        return bundles.update_bundle(settings, bundle_name, auth=self.auth)
