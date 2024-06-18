import ayon_api
from .auth import default_auth
import requests


# studio presets
def get_studio_anatomy_presets_names() -> list:
    """
    Возвращает список анатомии пресетов студии
    """
    data = ayon_api.get_project_anatomy_presets()
    return data

def get_studio_anatomy_preset(preset_name: str = None) -> dict:
    """
    Возвращает настройки конкретной анатомии пресета или PRIMARY, если не указано наименование пресета
    """
    data = ayon_api.get_project_anatomy_preset(preset_name)
    return data


def set_studio_anatomy_preset(preset_name: str, preset: dict):
    """
    Функция загружает настройки(в формате JSON) в конкретный пресет анатомии
    """
    url = f"{auth.SERVER_URL}/api/anatomy/presets/{preset_name}"
    response = requests.put(url=url, headers=auth.HEADERS, json=preset)
    response.raise_for_status()


def create_studio_anatomy_preset(preset_name: str, preset: dict):
    """
    Функция создает пресет анатомии
    """
    url = f"{auth.SERVER_URL}/api/anatomy/presets/{preset_name}"
    response = requests.put(url=url, headers=auth.HEADERS, json=preset)
    response.raise_for_status()


# project anatomy
def get_project_anatomy(project_name: str, auth=default_auth) -> dict:
    """
    Функция возвращает анатомию конкретного проекта
    """
    url = f"{auth.SERVER_URL}/api/projects/{project_name}/anatomy"
    response = requests.get(url=url, headers=auth.HEADERS)
    response.raise_for_status()
    return response.json()


def set_project_anatomy(project_name: str, anatomy: dict):
    url = f"{auth.SERVER_URL}/api/projects/{project_name}/anatomy"
    response = requests.post(url=url, headers=auth.HEADERS, json=anatomy)
    response.raise_for_status()
