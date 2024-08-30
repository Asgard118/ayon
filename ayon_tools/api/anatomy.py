import json
import logging

import ayon_api
from .auth import default_auth, Auth
import requests

from ..exceptipns import AnatomyConflictError, AnatomyUpdateError


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
    existing_anatomy = get_project_anatomy(project_name, auth=auth)
    anatomy = merge_anatomy_types(existing_anatomy, anatomy)
    url_post = f"{auth.SERVER_URL}/api/projects/{project_name}/anatomy"
    response = requests.post(
        url=url_post,
        headers=auth.HEADERS,
        json=anatomy,
    )

    if not response.ok:
        try:
            detail = response.json().get("detail", "Unknown error")
        except json.JSONDecodeError:
            detail = response.text
        if "is still referenced from table" in detail:
            raise AnatomyConflictError(detail)
        elif "" in detail:
            ...
        raise AnatomyUpdateError(detail)


def merge_anatomy_types(current_anatomy: dict, new_anatomy: dict):
    """
    Данная функция делает слияние анатомий с целью избежать удаление уже существующих типов которые используются в проектах.
    Это сделано чтобы избежать ошибки удаления используемых типов.
    Например:
    ayon_tools.exceptipns.AnatomyConflictError: name 'Compose' is still referenced from table "tasks".

    TODO: проверить какие типы реально используются а какие можно удалить.
    """

    existing_folder_types = {
        x["name"]: x for x in current_anatomy.get("folder_types", [])
    }
    new_folder_types = {x["name"]: x for x in new_anatomy.get("folder_types", [])}
    existing_folder_types.update(new_folder_types)
    new_anatomy["folder_types"] = list(existing_folder_types.values())

    existing_task_types = {x["name"]: x for x in current_anatomy.get("task_types", [])}
    new_task_types = {x["name"]: x for x in new_anatomy.get("task_types", [])}
    existing_task_types.update(new_task_types)
    new_anatomy["task_types"] = list(existing_task_types.values())

    existing_statuses = {x["name"]: x for x in current_anatomy.get("statuses", [])}
    new_statuses = {x["name"]: x for x in new_anatomy.get("statuses", [])}
    existing_statuses.update(new_statuses)
    new_anatomy["statuses"] = list(existing_statuses.values())
    return new_anatomy


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
