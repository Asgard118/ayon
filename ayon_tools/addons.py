from ayon_api import get_addons_project_settings, get_addons_settings

# studio addon settings
def get_studio_settings(bundle_name: str) -> dict:
    """
    Возвращает студийные настройки конкретного бандла
    """
    data = get_addons_settings(bundle_name)
    return data

def set_studio_settings(addon_name: str, version: str, settings: dict): ...


# project settings
def get_project_settings(project_name: str) -> dict:
    """
    Возвращает настройки аддонов конкретного проекта
    """
    data = get_addons_project_settings(project_name)
    return data
def set_project_settings(project_name: str, settings: dict): ...

