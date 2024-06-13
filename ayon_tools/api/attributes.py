from ayon_api import get_attributes_schema, set_attribute_config
from .auth import auth
import requests
def get_attributes() -> dict:
    """
    Функция возвращает список атрибутов
    """
    data = get_attributes_schema()
    return data
def set_attributes(attribute: str, data: dict):
    """
    Функцию обновляет конфигурацию конкретного аттрибута
    """
    response = requests.put(url=f'{auth.SERVER_URL}/api/attributes/{attribute}', headers=auth.HEADERS, json=data)
    return response.raise_for_status()
def create_attribute(data: dict):
    """
    Создает атрибут
    """
    response = requests.put(url=f'{auth.SERVER_URL}/api/attributes', headers=auth.HEADERS, json=data)
    return response.raise_for_status()
