from __future__ import annotations

import logging
import re
import sys
from typing import TYPE_CHECKING
from pathlib import Path
from ayon_tools.repository import repo, Repository
import ayon_tools
import subprocess

if TYPE_CHECKING:
    from ayon_tools.studio import StudioSettings


class Addon:
    addon_custom_attributes = "addons/{addon_name}/attributes.yml"
    custom_addon_shortcut_name = "settings.yml"

    def __init__(self, name, studio: StudioSettings, **kwargs):
        self.name = name
        self.studio = studio
        self.kwargs = kwargs

    def get_info_file(self):
        conf = repo.get_file_content(
            f"addons/{self.name}/info.yml", branch=self.studio.name, default=None
        )
        if not conf:
            conf = repo.get_file_content(
                f"addons/{self.name}/info.yml", branch="main", default=None
            )  # TODO default studio name from conf
        if not conf:
            raise ...
        # check
        assert conf.get("url"), f'Url not defined in addon config "{self.name}"'
        return conf

    def get_versions(self):
        rep = Repository(self.url)
        tags = rep.get_tags()
        versions = [tag for tag in tags if re.match(r"\d+\.\d+\.\d+.*", tag)]
        return versions

    @property
    def url(self):
        return self.get_addon_info()["url"]

    def get_default_settings(self, addon_ver: str):
        return self.studio.get_addon_default_settings(self.name, addon_ver)

    def get_repo_settings(self, project=None):
        # get default
        bundle = self.studio.get_rep_bundle()
        version = bundle["addons"][self.name]
        settings = self.get_default_settings(version)
        # resolve shortcuts
        settings = self.solve_shortcuts(settings, project)
        return settings

    def get_server_settings(self, version):
        return self.studio.get_addon_settings(self.name, version)

    def solve_shortcuts(self, settings: dict, project: str = None):
        # TODO: apply shortcuts
        # TODO: apply project shortcuts
        return settings

    def get_project_shortcut_settings(self, project_name: str):
        file_settings = repo.get_file_content(
            f"{project_name}/addons/{self.name}.yml", None
        )
        if not file_settings:
            return repo.get_file_content(
                f"{project_name}/addons/{self.name}/{self.custom_addon_shortcut_name}",
                None,
            )
        return file_settings

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
                logging.debug(f"Return addon class from default addons: {addon_name}")
                return _cls
        # base class
        logging.debug(f"Return base addon class: {addon_name}")
        return Addon

    @classmethod
    def get_addon_instance(cls, addon_name: str, studio: StudioSettings, **kwargs):
        addon_class = cls.get_addon_class(addon_name, studio)
        return addon_class(addon_name, studio, **kwargs)

    def get_addon_info(self) -> dict:
        info = repo.get_file_content(
            f"addons/{self.name}/info.yml", branch=self.studio.name
        )
        assert info["name"] == self.name
        return info

    def get_repository_url(self) -> str:
        return self.get_addon_info()["url"]

    def build(self, version) -> str:
        logging.info(f"Build addon {self.name} v{version}")
        rep = Repository(self.url)
        rep.reload()
        rep.set_tag(version)
        create_package_script = rep.workdir / "create_package.py"
        subprocess.run(
            [sys.executable, create_package_script], capture_output=True, text=True
        )
        build_dir = rep.workdir.joinpath("package")
        logging.info(f"Build dir: {build_dir}")
        zip_file = next(build_dir.glob(f"*{version}.zip"))

        return zip_file
