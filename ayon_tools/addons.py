from ayon_api import get_addons_project_settings, get_addons_settings
import requests
from .auth import auth

# studio addon settings
def get_studio_settings(bundle_name: str) -> dict:
    """
    Возвращает студийные настройки конкретного бандла
    """
    data = get_addons_settings(bundle_name)
    return data

def set_studio_settings(addon_name: str, version: str, settings: dict):
    """
    Обновление конкретной версии аддона, по определенным настройкам
    """
    response = requests.post(url=f'{auth.SERVER_URL}/api/addons/{addon_name}/{version}/settings', headers=auth.HEADERS, json=settings)
    return response.raise_for_status


# project settings
def get_project_settings(project_name: str) -> dict:
    """
    Возвращает настройки аддонов конкретного проекта
    """
    data = get_addons_project_settings(project_name)
    return data
def set_project_settings(addon_name: str, version: str, project_name: str, settings: dict):
    """
    Обновляет конкретную версию аддона проекта
    """
    response = requests.post(url=f'{auth.SERVER_URL}/api/addons/{addon_name}/{version}/settings/{project_name}', headers=auth.HEADERS, json=settings)
    return response.raise_for_status


