from typing import Any
import requests
import ayon_api
from .auth import auth


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


def check_attribute_exists(name: str) -> bool:
    """
    Проверяет наличие атрибута по имени
    """
    attributes = get_attributes()
    for attribute in attributes['attributes']:
        if isinstance(attribute, dict) and attribute.get('name') == name:
            return True
    return False


def create_attribute(
        name: str,
        title: str,
        scope: list,
        description: str = None,
        builtin: bool = True,
        data_type: str = 'string',
        example: Any = None,
        options: dict = None
        ):
    """
    Создает атрибут

    Options:
    {
        "default": 25,
        "gt": 0,
        "ge": null,
        "lt": null,
        "le": null,
        "minLength": null,
        "maxLength": null,
        "minItems": null,
        "maxItems": null,
        "regex": null,
        "enum": null,
        "inherit": true
    }
    """
    if check_attribute_exists(name):
        raise NameError(f'Attribute "{name}" already exists')
    creation_data = {
      "name": name,
      "position": 0,
      "scope": check_attr_scope(scope),
      "builtin": builtin,
      "data": {
        "type": _check_attr_date_type(data_type),
        "title": title,
        "example": example or '',
        "description": description or "",
        **(options or {})
        }
    }
    response = requests.put(url=f'{auth.SERVER_URL}/api/attributes', headers=auth.HEADERS, json=creation_data)
    return response.raise_for_status()


def _check_attr_date_type(data_type):
    # TODO
    return data_type


def check_attr_scope(scope):
    # TODO
    return scope
