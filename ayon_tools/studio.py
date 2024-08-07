import logging

import ayon_api

import re

from . import api
from . import config
from .repository import repo
from .api import system



class StudioSettings:
    bundle_config_file = "bundle.yml"
    anatomy_config_file = "defaults/anatomy.json"
    attributes_config_file = "attributes.yml"
    studio_config_file = "addons/{addon_name}/defaults.json"
    project_settings_file = "projects/{project}/project_settings.json"
    project_anatomy_file = "projects/{project}/project_anatomy.json"
    anatomy_preset_default_name = "default"

    def __init__(self, name: str, **kwargs):
        self.name = name
        studio_config = self.get_config_data()
        self.auth = api.auth.Auth(**studio_config)
        self.server_info = self.get_server_version()


    def get_server_version(self):
        server_info = system.get_server_info()
        server_version = re.split(r'\+', server_info)[0]
        return server_version

    def __str__(self):
        return f'StudioSettings("{self.name}")'

    def __repr__(self):
        return f'<StudioSettings "{self.name}">'

    def get_config_data(self):
        studio_local_config = config.get_studio_local_config(self.name)
        if (
            "server_url" not in studio_local_config
            or "token" not in studio_local_config
        ):
            raise ValueError("Invalid config file")
        return studio_local_config

    # SERVER ##################################################################

    def get_server_addons_settings(self):
        return api.addons.get_addons_settings(auth=self.auth)

    def get_projects(self):
        return api.projects.get_projects(auth=self.auth)

    def get_project_names(self):
        return api.projects.get_project_names(auth=self.auth)

    # studio addon settings

    def get_addons(self):
        return api.addons.get_studio_settings(auth=self.auth)

    def get_addon_settings(self, name: str, ver: str):
        return api.addons.get_addon_studio_settings(name, ver, auth=self.auth)

    def get_addons_settings(self):
        return api.addons.get_addons_settings(auth=self.auth)

    def set_addon_settings(self, name: str, ver: str, settings: dict):
        api.addons.set_studio_settings(name, ver, settings)

    # anatomy

    def get_anatomy_presets(self):
        """
        Список пресетов анатомии
         [
            {'name': 'preset_name',
             'primary': False,
             'version': '1.0.0'
             },
             ...
         ]
        """
        return api.anatomy.get_studio_anatomy_presets(auth=self.auth)

    def get_anatomy_preset_names(self):
        """
        Список имён пресетов анатомии
         [
            'preset_name1',
            'preset_name2',
            ...
         ]
        """
        presets = self.get_anatomy_presets()
        return [preset["name"] for preset in presets]

    def get_builtin_anatomy_preset(self):
        """
        Базовый пресет анатомии
        """
        return api.anatomy.get_build_in_anatomy_preset(auth=self.auth)

    def get_anatomy_preset(self, preset_name: str = None):
        """
        Получение пресета анатомии
        """
        if not preset_name:
            return self.get_default_anatomy_preset()
        if preset_name not in self.get_anatomy_preset_names():
            raise NameError(f"Preset named {preset_name} not exists")
        return api.anatomy.get_studio_anatomy_preset(preset_name, auth=self.auth)

    def create_anatomy_preset(self, preset_name: str, preset_data: dict = None):
        """
        Создание нового пресета анатомии
        Если не указать данные пресета то будет использоваться базовый built-in пресет
        """
        if preset_name in self.get_anatomy_preset_names():
            raise NameError(f"Preset named {preset_name} already exists")
        preset_data = preset_data or self.get_builtin_anatomy_preset()
        return api.anatomy.create_studio_anatomy_preset(
            preset_name, preset_data, auth=self.auth
        )

    def delete_anatomy_preset(self, preset_name: str):
        """
        Удаление пресета анатомии
        """
        return api.anatomy.delete_anatomy_preset(preset_name, auth=self.auth)

    def update_anatomy_preset(self, preset_name: str, preset_data: dict):
        """
        Обновление пресета анатомии. Данные должны быть полностью совместимы с AYON Server API
        """
        if preset_name not in self.get_anatomy_preset_names():
            raise NameError(f"Preset named {preset_name} not exists")
        return api.anatomy.set_studio_anatomy_preset(
            preset_name, preset_data, auth=self.auth
        )

    def set_primary_anatomy_preset(self, preset_name: str):
        """
        Сделать пресет PRIMARY
        """
        if preset_name not in self.get_anatomy_preset_names():
            raise NameError(f"Preset named {preset_name} not exists")
        return api.anatomy.set_primary_preset(preset_name, auth=self.auth)

    def get_default_anatomy_preset(self):
        """
        Возвращает данные дефолтного пресета студии
        """
        try:
            name = self.get_default_anatomy_preset_name()
        except NameError:
            name = self.create_default_anatomy_preset()
        return self.get_anatomy_preset(name)

    def get_default_anatomy_preset_name(self):
        """
        Возвращает имя дефолтного пресета студии если он есть на сервере
        """
        existing_names = self.get_anatomy_preset_names()
        if self.anatomy_preset_default_name not in existing_names:
            raise NameError(
                f"Default preset {self.anatomy_preset_default_name} not found"
            )
        return self.anatomy_preset_default_name

    def create_default_anatomy_preset(self):
        """
        Создает дефолтный пресет анатомии если его нет на сервере
        """
        if self.anatomy_preset_default_name in self.get_anatomy_preset_names():
            raise NameError(
                f"Default preset {self.anatomy_preset_default_name} already exists"
            )
        self.create_anatomy_preset(self.anatomy_preset_default_name)
        self.set_primary_anatomy_preset(self.anatomy_preset_default_name)
        return self.anatomy_preset_default_name

    # attributes
    def get_attributes(self):
        return api.attributes.get_attributes(auth=self.auth)

    def set_attributes(self, attributes: dict):
        for attr, data in attributes.items():
            api.attributes.set_attributes(attr, data, auth=self.auth)

    def set_attributes_config(self, *args, **kwargs):
        api.attributes.update_attributes_config(*args, **kwargs)

    def set_all_attributes(self, data: dict):
        api.attributes.set_all_attributes(data, auth=self.auth)

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

    def create_bundle(self, name: str, addons, installer_version, **options):
        # installer_version: str = data["installerVersion"]
        # addon_list = data["addons"]
        return api.bundles.create_bundle(
            name, addons, installer_version, auth=self.auth, **options
        )

    def create_new_bundle(self, data: dict, bundle_name: str):
        return api.bundles.create_new_bundles(data, bundle_name, auth=self.auth)

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

    def update_project(self, *args, **kwargs):
        return api.addons.update_project(auth=self.auth, *args, **kwargs)

    #  REPOSITORY ################################################################
    # anatomy

    def get_rep_anatomy(self, project: str = None):
        """
        Актуальный пресет анатомии из репозитория
        """
        cls = self.get_shortcut_solver_class("anatomy")
        return cls(self).solve(project)

    def get_rep_bundle(self):
        """
        Актуальный состав бандла из репозитория
        """
        bundle = repo.get_file_content(self.bundle_config_file, self.name)
        return bundle

    # def get_rep_addon_settings(self, addon_name: str, project: str = None):
    #     """
    #     Актуальные студийные настройки аддона из репозитория
    #     """
    #     addons = repo.get_file_content(
    #         self.studio_config_file.format(addon_name=addon_name), self.name, None
    #     )
    #     if project:
    #         from . import tools
    #
    #         try:
    #             project_addons = repo.get_file_content(
    #                 self.project_settings_file.format(project=project), self.name
    #             )
    #         except FileNotFoundError:
    #             logging.debug("No project overrides")
    #         # else:
    #         #     tools.update_dict_with_changes(addons, project_addons)
    #     return addons

    def get_rep_attributes(self):
        """
        Актуальные студийные атрибуты из репозитория
        """
        # from studio
        attributes = repo.get_file_content(
            self.attributes_config_file, self.name, default=[]
        )
        # from addons
        addon_list = self.get_rep_bundle()
        addons = addon_list.get("addons", [])
        for addon_name in addons.keys():
            addon = self.get_addon(addon_name)
            addon_atts = addon.get_custom_attributes()
            if addon_atts:
                attributes.extend(addon_atts)
        # prepare data
        for attr in attributes:
            api.attributes.update_default_data(attr)
        api.attributes.validate_attributes(attributes)
        dict_attributes = {"attributes": attributes}
        return dict_attributes

    def get_rep_addon_attributes(self) -> list: ...

    # project from repo

    def get_rep_project_addons(self):
        """
        Настройки всех аддонов проекта.
        Структура настроек должна подходить под указанные в бандле версии
        """
        # TODO

    # utils
    def get_addon(self, addon_name: str):
        from . import base_addon

        return base_addon.Addon.get_addon_instance(addon_name, self)

    def get_shortcut_solver_class(self, module_name: str, project_name: str = None):
        """
        Функция возвращает класс солвера по имени модуля.
        Сначала ищет в проекте, потом в студии. Если не найдено то возвращает стандартный солвер.
        Поиск происходит в директории shortcut_solvers
        """
        from .base_shortcut_solver import Solver

        from .tools import (
            import_subclasses_from_string_module,
            import_module_from_dotted_path,
            get_subclass_from_module,
        )

        cls = None
        if project_name:
            project_anatomy_module_path = (
                f"projects/{project_name}/shortcut_solvers/{module_name}.py"
            )
            custom_module = repo.get_file_content(
                project_anatomy_module_path, branch=self.name, default=None
            )
            if custom_module:
                logging.debug(
                    "Looking for custom anatomy preset class from project overrides..."
                )
                cls = next(
                    import_subclasses_from_string_module(
                        custom_module,
                        f"{self.name.title()}{project_name.title()}{module_name.title()}",
                        Solver,
                    ),
                    None,
                )
                if cls:
                    logging.debug(
                        "Using custom anatomy preset class from project overrides"
                    )
                    return cls
        anatomy_module_path = f"shortcut_solvers/{module_name}.py"
        custom_module = repo.get_file_content(
            anatomy_module_path, branch=self.name, default=None
        )
        if custom_module:
            logging.debug(
                "Looking for custom anatomy preset class from studio overrides..."
            )
            cls = next(
                import_subclasses_from_string_module(
                    custom_module, f"{self.name.title()}{module_name.title()}", Solver
                ),
                None,
            )
            if cls:
                logging.debug("Using custom anatomy preset class from studio overrides")
                return cls
        default_module = ".".join(
            __name__.split(".")[:-1] + ["shortcut_solvers", module_name]
        )
        logging.debug(f"Importing default module {default_module}")
        module = import_module_from_dotted_path(default_module)
        cls = next(get_subclass_from_module(module, Solver), None)
        if cls:
            logging.debug("Using default shortcut solver class from main package")
            return cls
        else:
            raise NameError(f'Solver module "{module_name}" not found')
