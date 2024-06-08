from ayon_api import get_project_anatomy_presets, get_project_anatomy_preset
from .auth import auth
import requests

# studio presets
def get_studio_anatomy_presets_names() -> list:
    """
    Возвращает список анатомии пресетов студии
    """
    data = get_project_anatomy_presets()
    return data
def get_studio_anatomy_preset(preset_name: str = None) -> dict:
    """
    Возвращает настройки конкретной анатомии пресета или PRIMARY, если не указано наименование пресета
    """
    data = get_project_anatomy_preset(preset_name)
    return data
def set_studio_anatomy_preset(preset_name: str, preset: dict):
    """
    Функция загружает настройки(в формате JSON) в конкретный пресет анатомии
    """
    url = f"{auth.SERVER_URL}/api/anatomy/presets/{preset_name}"
    response = requests.put(url=url, headers=auth.HEADERS, json=preset)
    if response.status_code == 204:
        print("Preset updated successfully.")
    else:
        print(response.content)
def create_studio_anatomy_preset(preset_name: str, preset: dict): ...


# project anatomy
def get_project_anatomy(project_name: str) -> dict: ...
def set_project_anatomy(project_name: str, anatomy: dict): ...

