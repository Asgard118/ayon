import ayon_api
from .auth import auth
import requests


def get_attributes() -> dict:
    """
    Функция возвращает список атрибутов
    """
    data = ayon_api.get_attributes_schema()
    return data


def set_attributes(attribute: str, data: dict):
    """
    Функцию обновляет конфигурацию конкретного аттрибута
    """
    response = requests.put(url=f'{auth.SERVER_URL}/api/attributes/{attribute}', headers=auth.HEADERS, json=data)
    return response.raise_for_status()


def check_attribute(name: str):
    """
    Проверяет наличие атрибута по имени
    """
    attributes = get_attributes()
    for attribute in attributes['attributes']:
        if isinstance(attribute, dict) and attribute.get('name') == name:
            return attribute
    return None


def create_attribute(data: dict):
    """
    Создает атрибут
    """
    response = requests.put(url=f'{auth.SERVER_URL}/api/attributes', headers=auth.HEADERS, json=data)
    return response.raise_for_status()
