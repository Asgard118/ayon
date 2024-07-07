from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from pathlib import Path
from ayon_tools.repository import repo
import ayon_tools

if TYPE_CHECKING:
    from ayon_tools.studio import StudioSettings


class Addon:
    addon_custom_attributes = "addons/{addon_name}/attributes.yml"

    def __init__(self, name, studio: StudioSettings, **kwargs):
        self.name = name
        self.studio = studio
        self.kwargs = kwargs

    def get_default_settings(self, studio_name: str):
        default_settings_path = Path("addons", self.name, "defaults.json").as_posix()
        return repo.get_file_content(default_settings_path, studio_name)

    def get_repo_settings(self, studio_name):
        settings_path = Path("addons", self.name, "defaults.json").as_posix()
        return repo.get_file_content(settings_path, studio_name)

    def get_settings(self, studio_name: str = None, project: str = None):
        # get default
        settings = self.get_default_settings(studio_name)
        # resolve shortcuts
        settings = self.solve_shortcuts(settings, project)
        return settings

    def build(self) -> str: ...

    def solve_shortcuts(self, settings: dict, project: str = None):
        # TODO: apply shortcuts
        # TODO: apply project shortcuts
        return settings

    def get_custom_attributes(self):
        attrs = []
        # from default
        attr_path = Path(
            Path(ayon_tools.__file__).parent, "addons", self.name, "attributes.yml"
        )
        if attr_path.exists():
            import yaml

            with attr_path.open("r") as stream:
                default_attrs = yaml.safe_load(stream)
            if default_attrs:
                if not isinstance(default_attrs, list):
                    raise TypeError("Attributes must be a list")
                attrs.extend(default_attrs)
        # from repo
        repo_attrs = repo.get_file_content(
            self.addon_custom_attributes.format(addon_name=self.name),
            self.studio.name,
            default=None,
        )
        if repo_attrs:
            if not isinstance(repo_attrs, list):
                raise TypeError("Attributes must be a list")
            attrs.extend(repo_attrs)
        return attrs

    @classmethod
    def get_addon_class(cls, addon_name: str, studio: StudioSettings):
        from ayon_tools.tools import (
            import_subclasses_from_string_module,
            import_subclasses_from_path_module,
        )
        import ayon_tools

        # from studio override
        data = repo.get_file_content(
            f"addons/{addon_name}/addon.py", branch=studio.name, default=None
        )
        if data:
            for _cls in import_subclasses_from_string_module(
                data, f"{addon_name}_{studio.name}_addon_module", Addon
            ):
                logging.info(f"Return addon class from repository: {addon_name}")
                return _cls
        # from default addon list
        module_path = (
            Path(ayon_tools.__file__).parent / "addons" / addon_name / "addon.py"
        )
        if module_path.exists():
            _cls = next(import_subclasses_from_path_module(module_path, Addon), None)
            if _cls:
                logging.info(f"Return addon class from default addons: {addon_name}")
                return _cls
        # base class
        logging.info(f"Return base addon class: {addon_name}")
        return Addon

    @classmethod
    def get_addon_instance(cls, addon_name: str, studio: StudioSettings, **kwargs):
        addon_class = cls.get_addon_class(addon_name, studio)
        return addon_class(addon_name, studio, **kwargs)
