from ayon_tools.base_addon import Addon
from ayon_tools.repository import repo
from pathlib import Path
import json

class ApplicationsAddon(Addon):

    def transform_data(self, input_data):
        transformed_data = {}

        for item in input_data:
            name = item['name']
            label = item['label']
            versions = item['versions']

            transformed_data[name] = {
                'enabled': True,
                'environment': '{\n'
                               '  "MAYA_DISABLE_CLIC_IPM": "Yes",\n'
                               '  "MAYA_DISABLE_CIP": "Yes",\n'
                               '  "MAYA_DISABLE_CER": "Yes",\n'
                               '  "PYMEL_SKIP_MEL_INIT": "Yes",\n'
                               '  "LC_ALL": "C"\n'
                               '}\n',
                'host_name': name,
                'icon': '{}/app_icons/maya.png',  # Укажите правильный путь к иконке
                'label': label,
                'variants': []
            }

            for version in versions:
                executables = {
                    'windows': [version['executables']['windows']] if version.get('executables') and version[
                        'executables'].get('windows') else ['C:\\AppData\\Autodesk\\Maya2024\\bin\\maya.exe'],
                    'darwin': [version['executables']['darwin']] if version.get('executables') and version[
                        'executables'].get('darwin') else ['/Applications/Autodesk/maya2024/Maya.app'],
                    'linux': [version['executables']['linux']] if version.get('executables') and version[
                        'executables'].get('linux') else ['/usr/autodesk/maya2024/bin/maya']
                }

                variant = {
                    'name': version['name'],
                    'label': version['name'],
                    'environment': json.dumps({
                        'MAYA_VERSION': version['name']
                    }),
                    'executables': executables,
                    'arguments': {
                        'windows': [],
                        'darwin': [],
                        'linux': []
                    },
                    'use_python_2': False
                }

                transformed_data[name]['variants'].append(variant)

        return transformed_data

    def get_repo_settings_for_applications(self, project_name: str = None):
        new_settings = (
            repo.get_file_content(Path("projects", project_name, "folders.yml").as_posix(), default={}
            )
            if project_name
            else {}
        ) or repo.get_file_content('applications.yml')
        default_settings = self.get_default_settings(self.studio.name)
        settings = self.transform_data(new_settings)
        return settings