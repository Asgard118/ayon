import logging

import ayon_api
from .auth import default_auth, Auth
import requests


# studio presets
def get_studio_anatomy_presets(auth: Auth = default_auth) -> list:
    """
    Возвращает список анатомии пресетов студии
    """
    with auth:
        data = ayon_api.get_project_anatomy_presets()
    return data


def get_studio_anatomy_preset(
    preset_name: str = None, auth: Auth = default_auth
) -> dict:
    """
    Возвращает настройки конкретной анатомии пресета или PRIMARY, если не указано наименование пресета
    """
    with auth:
        data = ayon_api.get_project_anatomy_preset(preset_name)
    return data


def get_build_in_anatomy_preset(auth: Auth = default_auth) -> dict:
    with auth:
        data = ayon_api.get_build_in_anatomy_preset()
    return data


def set_studio_anatomy_preset(
    preset_name: str,
    preset: dict,
    auth: Auth = default_auth,
):
    """
    Функция загружает настройки(в формате JSON) в конкретный пресет анатомии
    """
    url_put = f"{auth.SERVER_URL}/api/anatomy/presets/{preset_name}"
    response = requests.put(url=url_put, headers=auth.HEADERS, json=preset)
    return response.raise_for_status()


def create_studio_anatomy_preset(
    preset_name: str, preset: dict, auth: Auth = default_auth
):
    """
    Функция создает пресет анатомии
    """
    url_put = f"{auth.SERVER_URL}/api/anatomy/presets/{preset_name}"
    response = requests.put(
        url=url_put,
        headers=auth.HEADERS,
        json=preset,
    )
    response.raise_for_status()


def delete_anatomy_preset(preset_name: str, auth: Auth = default_auth):
    url_delete = f"{auth.SERVER_URL}/api/anatomy/presets/{preset_name}"
    response = requests.delete(
        url=url_delete,
        headers=auth.HEADERS,
    )
    response.raise_for_status()


# project anatomy
def get_project_anatomy(project_name: str, auth: Auth = default_auth) -> dict:
    """
    Функция возвращает анатомию конкретного проекта
    """
    url_get = f"{auth.SERVER_URL}/api/projects/{project_name}/anatomy"
    response = requests.get(
        url=url_get,
        headers=auth.HEADERS,
    )
    response.raise_for_status()
    return response.json()


def set_project_anatomy(project_name: str, anatomy: dict, auth: Auth = default_auth):
    url_post = f"{auth.SERVER_URL}/api/projects/{project_name}/anatomy"
    response = requests.post(
        url=url_post,
        headers=auth.HEADERS,
        json=anatomy,
    )

    if not response.ok:
        try:
            resp_data = response.json()
            logging.error(resp_data.get("detail", "Unknown"))
        except Exception:
            resp_data = response.text
            logging.error(resp_data)
    response.raise_for_status()


def set_primary_preset(preset_name: str, auth: Auth = default_auth):
    url_post = f"{auth.SERVER_URL}/api/anatomy/presets/{preset_name}/primary"
    response = requests.post(
        url=url_post,
        headers=auth.HEADERS,
    )
    response.raise_for_status()


def get_anatomy_name(compare_name: str, rep_preset: dict, auth: Auth = default_auth):
    with auth:
        presets = get_studio_anatomy_presets()
        primary_preset = next((preset for preset in presets if preset["primary"]), None)
        if primary_preset:
            if primary_preset["name"] != compare_name:
                create_studio_anatomy_preset(compare_name, rep_preset)
                return compare_name
        else:
            create_studio_anatomy_preset(compare_name, rep_preset)
            return compare_name
