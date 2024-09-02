import ayon_api
import requests
from .auth import default_auth, Auth


# studio addon settings
def get_studio_settings(auth: Auth = default_auth) -> dict:
    """
    Возвращает студийные настройки конкретного бандла
    """
    with auth:
        data = ayon_api.get_addons_settings()
    return data


def get_addon_studio_settings(name: str, ver: str, auth: Auth = default_auth):
    """
    Возвращает студийные настройки конкретного аддона указанной версии
    """
    with auth:
        return ayon_api.get_addon_studio_settings(name, ver)


def get_addons_settings(auth: Auth = default_auth):
    with auth:
        return ayon_api.get_addons_studio_settings()

def get_installed_addon_list(auth: Auth = default_auth):
    response = requests.get(url=f"{auth.SERVER_URL}/api/addons/install", headers=auth.HEADERS)
    return response.json()

def set_studio_settings(
    addon_name: str, version: str, settings: dict, auth: Auth = default_auth
):
    """
    Обновление конкретной версии аддона, по определенным настройкам
    """
    response = requests.post(
        url=f"{auth.SERVER_URL}/api/addons/{addon_name}/{version}/settings",
        headers=auth.HEADERS,
        json=settings,
    )
    response.raise_for_status()


# project settings
def get_project_settings(project_name: str, auth: Auth = default_auth) -> dict:
    """
    Возвращает настройки аддонов конкретного проекта
    """
    with auth:
        data = ayon_api.get_addons_project_settings(project_name)
    return data


def set_project_settings(
    addon_name: str,
    version: str,
    project_name: str,
    settings: dict,
    auth: Auth = default_auth,
):
    """
    Обновляет конкретную версию аддона проекта
    """
    response = requests.post(
        url=f"{auth.SERVER_URL}/api/addons/{addon_name}/{version}/settings/{project_name}",
        headers=auth.HEADERS,
        json=settings,
    )
    response.raise_for_status()


def update_project(auth: Auth = default_auth, *args: any, **kwargs: any):
    with auth:
        return ayon_api.update_project(*args, **kwargs)

def install_addon(src_filepath, auth: Auth = default_auth):
    with auth:
        return ayon_api.upload_addon_zip(src_filepath)