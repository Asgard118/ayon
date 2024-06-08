import requests
import ayon_api
from .auth import auth


# BUNDLE

def get_bundle(bundle_name: str):
    """
    Возвращает состав бандла по имени
    {
        TODO: краткий пример здесь
    }
    """
    data = get_bundles()
    if 'bundles' in data:
        for bundle in data['bundles']:
            if bundle['name'] == bundle_name:
                return bundle['addons']
    return None


def get_bundles():
    """
    Возвращает список бандлов
    {
        TODO: краткий пример здесь
    }
    """
    return ayon_api.get_bundles()

def create_bundle(name: str, addons: dict):
    """
    Создает бандл с указанными аддонами
    """
    creation_data = {...}
    response = requests.post(f"{auth.SERVER_URL}/api/bundles",
                             headers=auth.HEADERS,
                             json=creation_data)

    response.raise_for_status()
    return response.json()


# PRESETS


# STUDIO SETTINGS

def set_studio_addon_settings(bundle_name: str, settings: dict):
    """
    Устанавливает студийные настройки для аддонов бандла
    """

# PROJECT SETTINGS

def get_project_addons_settings(project_name: str):
    """
    Возвращает настройки для аддонов проекта
    """
    return ayon_api.get_addons_project_settings(project_name)


def get_addons_setting(addon_name: str, bundle_name: str = None, project_name: str = None):
    """
    ?????
    """
    pro_data = ayon_api.get_addons_settings(project_name=project_name)
    studio_data = ayon_api.get_addons_settings(bundle_name=bundle_name)
    return {
      'project_settings': pro_data,
      'studio_settings': studio_data[addon_name]
    }

def get_project_anatomy():
    return ayon_api.get_project_anatomy_preset()
