from .api import anatomy, bundles, attributes, auth, addons
from . import config
from .repository import repo


class StudioSettings:
    bundle_config_file = "bundle/bundles_settings.json"
    anatomy_config_file = "anatomy/anatomy.json"
    attributes_config_file = "attributes/attributes.json"
    studio_config_file = "studio/studio_settings.json"
    project_settings = "projects/{project}/project_settings.json"
    project_anatomy = "projects/{project}/project_anatomy.json"


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

    def get_addons(self):
        return addons.get_studio_settings(auth=self.auth)

    def set_addon_settings(self, name: str, ver: str, settings: dict):
        addons.set_studio_settings(name, ver, settings)

    def get_anatomy(self, preset_name: str = None):
        return anatomy.get_studio_anatomy_preset(preset_name, auth=self.auth)

    def get_attributes(self):
        return attributes.get_attributes(auth=self.auth)

    def set_attributes(self, attribute: str, data: dict):
        return attributes.set_attributes(attribute, data, auth=self.auth)

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
            addon_name, addon_version, project_name, settings, auth=self.auth
        )

    def set_anatomy(self, preset_name: str, preset: dict):
        return anatomy.set_studio_anatomy_preset(preset_name, preset, auth=self.auth)

    def get_default_anatomy_name(self):
        return anatomy.get_anatomy_name(auth=self.auth)

    def update_project(self, *args, **kwargs):
        return addons.update_project(auth=self.auth, *args, **kwargs)



# studio from repo
    def get_rep_bundle(self):
        """
        Актуальный состав бандла из репозитория
        """
        bundle = repo.get_file_content(self.bundle_config_file, self.name)
        return bundle

    def get_rep_addons_settings(self, project: str = None):
        """
        Актуальные студийные настройки аддонов из репозитория
        """
        addons = repo.get_file_content(self.studio_config_file, self.name)
        if project:
            from . import tools
            project_addons = repo.get_file_content(self.project_settings.format(project=project), self.name)
            if not tools.compare_dicts(addons, project_addons):
                tools.update_dict_with_changes(addons, project_addons)
        return addons

    def get_rep_anatomy(self, project: str = None):
        """
        Актуальный пресет анатомии из репозитория
        """
        anatomy = repo.get_file_content(self.anatomy_config_file, self.name)
        if project:
            from . import tools
            project_anatomy = repo.get_file_content(self.project_anatomy.format(project=project), self.name)
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
