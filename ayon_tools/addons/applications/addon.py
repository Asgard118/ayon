from ayon_tools.base_addon import Addon
from ayon_tools.repository import repo


class ApplicationsAddon(Addon):
    _supported_apps = [
        "maya",
        "adsk_3dsmax",
        "flame",
        "nuke",
        "nukeassist",
        "nukex",
        "nukestudio",
        "hiero",
        "fusion",
        "resolve",
        "houdini",
        "blender",
        "harmony",
        "tvpaint",
        "photoshop",
        "aftereffects",
        "celaction",
        "substancepainter",
        "unreal",
        "wrap",
        "additional_apps",
    ]

    def solve_shortcuts(self, settings: dict, project: str = None):
        apps_settings = repo.get_file_content(
            "applications.yml", branch=self.studio.name, default=None
        )
        if not apps_settings:
            return settings

        # resolve app list
        enabled_apps = []
        for app in apps_settings:
            api_settings = self.convert_shortcut_app_to_settings_app(app)
            app_name = api_settings.pop("name")
            enabled_apps.append(app_name)
            apps_settings["applications"][app_name] = api_settings
        # disable not defined apps
        for app_name in list(settings["applications"].keys()):
            if app_name not in enabled_apps:
                settings["applications"][app_name]["enabled"] = False
        return settings

    def update_dictionary(self, existing_dict, new_data):
        if "applications" not in existing_dict:
            existing_dict["applications"] = {}

        for app in new_data:
            app_name = app["name"]
            if app_name in existing_dict["applications"]:
                if "label" in app:
                    existing_dict["applications"][app_name]["label"] = app["label"]

                if "versions" in app:
                    existing_dict["applications"][app_name]["variants"] = []
                    for version in app["versions"]:
                        variant = {
                            "name": version["name"],
                            "label": version.get("label", version["name"]),
                            "executables": {"windows": [], "linux": [], "darwin": []},
                            "arguments": {"windows": [], "linux": [], "darwin": []},
                            "environment": "{}",
                            "use_python_2": False,
                        }

                        if "executables" in version:
                            if isinstance(version["executables"], dict):
                                for platform, path in version["executables"].items():
                                    variant["executables"][platform] = [path]
                            elif isinstance(version["executables"], str):
                                variant["executables"]["windows"] = [
                                    version["executables"]
                                ]

                        existing_dict["applications"][app_name]["variants"].append(
                            variant
                        )
            else:
                # принт на время теста функции добавил, для ясности
                print(f"addon {app_name} not found in settings")

        return existing_dict

    def convert_shortcut_app_to_settings_app(self, shortcut_app: dict):
        """
        SOURCE DATA ==================================

        - name: maya
          label: Maya
          versions:
            - name: 2024
            - name: 2025

        TARGET DATA ==================================
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
        if shortcut_app["name"] not in self._supported_apps:
            raise Exception(f"Unsupported application name: '{shortcut_app['name']}'")
        settings = {**shortcut_app}  # TODO

        return settings