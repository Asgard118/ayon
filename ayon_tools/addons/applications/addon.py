import json
import logging

from ayon_tools.base_addon import Addon
from ayon_tools.repository import repo
from .variants import get_variant_class


class ApplicationsAddon(Addon):

    def solve_shortcuts(self, settings: dict, project: str = None):
        shortcut_apps = repo.get_file_content(
            "applications.yml", branch=self.studio.name, default=None
        )
        if not shortcut_apps:
            return settings
        shortcut_apps = {app["name"]: app for app in shortcut_apps}
        # resolve app list
        for app_name, app_data in settings["applications"].items():
            if not isinstance(app_data, dict):
                continue
            if app_name in shortcut_apps:
                updated_data = self.convert_shortcut_app_to_settings_app(
                    app_data, shortcut_apps[app_name]
                )
                updated_data["enabled"] = True
                settings["applications"][app_name] = updated_data
            else:
                settings["applications"][app_name]["enabled"] = False
        return settings

    def convert_shortcut_app_to_settings_app(
        self,
        settings_app: dict,
        shortcut_app: dict,
    ):
        """
        shortcut_app ==================================

        - name: maya
          label: Maya
          versions:
            - 2024
            - 2025

        settings_app ==================================
        {
          "name": "maya",   // will removed later
          "enabled": true,
          "label": "Maya",
          "host_name": "maya",
          "icon": "{}/app_icons/maya.png",
          "environment": "{\n  \"MAYA_DISABLE_CLIC_IPM\": \"Yes\",\n  \"MAYA_DISABLE_CIP\": \"Yes\",\n  \"MAYA_DISABLE_CER\": \"Yes\",\n  \"PYMEL_SKIP_MEL_INIT\": \"Yes\",\n  \"LC_ALL\": \"C\"\n}\n",
          "variants": [
            {
              "name": "2024",
              "label": "2024",
              "environment": "{\n  \"MAYA_VERSION\": \"2024\"\n}",
              "use_python_2": true,
              "executables": {
                "windows": [
                  "C:\\Program Files\\Autodesk\\Maya2022\\bin\\maya.exe"
                ],
                "linux": [
                  "/usr/autodesk/maya2022/bin/maya"
                ],
                "darwin": [
                  "/Applications/Autodesk/maya2022/Maya.app"
                ]
              },
              "arguments": {
                "windows": [],
                "linux": [],
                "darwin": []
              }
            },
            {
              "name": "2025",
              "label": "2025",
              "environment": "{}",
              "use_python_2": false,
              "executables": {
                "windows": [],
                "linux": [],
                "darwin": []
              },
              "arguments": {
                "windows": [],
                "linux": [],
                "darwin": []
              }
            }
          ]
        },
        """
        assert settings_app["name"] == shortcut_app["name"], "App name mismatch"
        # label
        if "label" in shortcut_app:
            settings_app["label"] = shortcut_app["label"]
        # envs
        current_env = settings_app["environment"]
        if "environment" in shortcut_app:
            current_env.update(shortcut_app["environment"])
        settings_app["environment"] = json.dumps(current_env)
        # variants
        variant_class = get_variant_class(settings_app["name"])
        if not variant_class:
            logging.error(f"Variant class not found for {settings_app['name']}")
            # raise Exception(f"Variant class not found for {settings_app['name']}")
        else:
            for variant_data in shortcut_app.get("versions", []):
                variant = variant_class(variant_data)
                settings_app["variants"].append(variant.get_config())
        # callback
        self.on_app_resolved(settings_app)
        return settings_app

    def on_app_resolved(self, settings):
        pass

    def get_app_list_attributes(self, project_name: str = None):
        """
        Example:
        [
          "hiero/15-0",
          "houdini/19-0",
          "maya/2023"
        ]
        """
        data = []
        # get settings
        app_list: dict = repo.get_file_content("project-settings.yml", default={}).get(
            "applications", []
        )
        if project_name:
            app_list: dict = (
                repo.get_file_content(
                    f"projects/{project_name}/project-settings.yml", default={}
                ).get("applications", [])
                or app_list
            )

        if not app_list:
            return data
        # get all registered apps
        all_apps = self.get_repo_settings().get("applications")
        for app_name, versions in app_list.items():
            if app_name not in all_apps:
                raise NameError(f"Application '{app_name}' not found in repository")
            for version in versions:
                all_variants = {
                    var["label"]: var["name"] for var in all_apps[app_name]["variants"]
                }
                version = str(version)
                if version not in all_variants:
                    raise NameError(
                        f"App Version '{app_name}/{version}' not found in registered application: {list(all_variants.keys())}"
                    )
                # add app attribute
                data.append(f"{app_name}/{all_variants[version]}")
        return data
