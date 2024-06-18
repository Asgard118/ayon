import ayon_api
import requests
from .auth import default_auth


# studio addon settings
def get_studio_settings(bundle_name: str, auth=default_auth) -> dict:
    """
    Возвращает студийные настройки конкретного бандла
    """
    with auth:
        data = ayon_api.get_addons_settings(bundle_name)
    return data


def set_studio_settings(addon_name: str, version: str, settings: dict, auth=default_auth):
    """
    Обновление конкретной версии аддона, по определенным настройкам
    """
    response = requests.post(url=f'{auth.SERVER_URL}/api/addons/{addon_name}/{version}/settings', headers=auth.HEADERS,
                             json=settings)
    return response.raise_for_status


# project settings
def get_project_settings(project_name: str) -> dict:
    """
    Возвращает настройки аддонов конкретного проекта
    """
    data = ayon_api.get_addons_project_settings(project_name)
    return data


def set_project_settings(addon_name: str, version: str, project_name: str, settings: dict, auth=default_auth):
    """
    Обновляет конкретную версию аддона проекта
    """
    response = requests.post(url=f'{auth.SERVER_URL}/api/addons/{addon_name}/{version}/settings/{project_name}',
                             headers=auth.HEADERS, json=settings)
    return response.raise_for_status
