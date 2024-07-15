from ayon_tools.base_addon import Addon
from ayon_tools.repository import repo
from pathlib import Path


class ApplicationsAddon(Addon):

    def update_dictionary(self, existing_dict, new_data):
        if 'applications' not in existing_dict:
            existing_dict['applications'] = {}

        for app in new_data:
            app_name = app['name']
            if app_name in existing_dict['applications']:
                if 'label' in app:
                    existing_dict['applications'][app_name]['label'] = app['label']

                if 'versions' in app:
                    existing_dict['applications'][app_name]['variants'] = []
                    for version in app['versions']:
                        variant = {
                            'name': version['name'],
                            'label': version.get('label', version['name']),
                            'executables': {
                                'windows': [],
                                'linux': [],
                                'darwin': []
                            },
                            'arguments': {
                                'windows': [],
                                'linux': [],
                                'darwin': []
                            },
                            'environment': "{}",
                            'use_python_2': False
                        }

                        if 'executables' in version:
                            if isinstance(version['executables'], dict):
                                for platform, path in version['executables'].items():
                                    variant['executables'][platform] = [path]
                            elif isinstance(version['executables'], str):
                                variant['executables']['windows'] = [version['executables']]

                        existing_dict['applications'][app_name]['variants'].append(variant)
            else:
                # принт на время теста функции добавил, для ясности
                print(f"addon {app_name} not found in settings")

        return existing_dict

    def solve_shortcuts(self, settings, project: str = None):
        new_settings = (
            repo.get_file_content(Path("projects", project, "folders.yml").as_posix(), default={}
            )
            if project
            else {}
        ) or repo.get_file_content('applications.yml')
        default_settings = self.get_default_settings(self.studio.name)
        settings = self.update_dictionary(default_settings, new_settings)
        return settings