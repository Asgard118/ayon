from typing import Any
import requests
import ayon_api
from .auth import default_auth, Auth
import yaml
import logging


def get_attributes(auth: Auth = default_auth):
    """
    Функция возвращает список атрибутов
    """
    response = requests.get(
        url=f"{auth.SERVER_URL}/api/attributes",
        headers=auth.HEADERS,
    )
    data = response.json()
    return data

def set_attributes(attribute: str, data: dict, auth: Auth = default_auth):
    """
    Функцию обновляет конфигурацию конкретного аттрибута
    """
    response = requests.put(
        url=f"{auth.SERVER_URL}/api/attributes/{attribute}",
        headers=auth.HEADERS,
        json=data,
    )
    response.raise_for_status()

def set_all_attributes(data: dict, auth: Auth = default_auth):
    response = requests.put(
        url=f"{auth.SERVER_URL}/api/attributes",
        headers=auth.HEADERS,
        json=data,
    )
    response.raise_for_status()

def check_attribute_exists(name: str) -> bool:
    """
    Проверяет наличие атрибута по имени
    """
    attributes = get_attributes()
    for attribute in attributes["attributes"]:
        if isinstance(attribute, dict) and attribute.get("name") == name:
            return True
    return False


def create_attribute(
    name: str,
    title: str,
    scope: list,
    description: str = None,
    builtin: bool = True,
    data_type: str = "string",
    example: Any = None,
    options: dict = None,
    auth: Auth = default_auth,
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
            "example": example or "",
            "description": description or "",
            **(options or {}),
        },
    }
    response = requests.put(
        url=f"{auth.SERVER_URL}/api/attributes",
        headers=auth.HEADERS,
        json=creation_data,
    )
    response.raise_for_status()


def _check_attr_date_type(data_type: str):
    """
    Проверяет соответствие типа атрибута
    """
    valid_data_types = [
        "string",
        "integer",
        "decimal number",
        "list of strings",
        "boolean",
    ]
    if data_type not in valid_data_types:
        raise ValueError(f"Invalid data type: {data_type}.")
    return data_type


def check_attr_scope(scope: list):
    """
    Проверяет соответствие типа области атрибута
    """
    valid_scopes = [
        "project",
        "folder",
        "task",
        "user",
        "product",
        "version",
        "representation",
    ]
    if not isinstance(scope, list):
        raise ValueError(f"Scope should be a list of valid values. Provided: {scope}")
    invalid_scopes = [s for s in scope if s not in valid_scopes]
    if invalid_scopes:
        raise ValueError(f"Invalid scope(s)")
    return scope


def validate_attributes_yaml(yaml_content):
    try:
        if isinstance(yaml_content, str):
            attributes = yaml.safe_load(yaml_content)
        elif isinstance(yaml_content, list):
            attributes = yaml_content
        else:
            raise ValueError("yaml_content should be a string or a list of dictionaries")
    except yaml.YAMLError as exc:
        raise ValueError(f"Error loading YAML: {exc}")

    for attribute in attributes:
        name = attribute.get('name')
        scope = attribute.get('scope')
        data = attribute.get('data', {})
        data_type = data.get('type')

        if scope:
            try:
                check_attr_scope(scope)
            except ValueError as e:
                logging.error(f"Error: {e}, attributes {name}")

        if data_type:
            try:
                _check_attr_date_type(data_type)
            except ValueError as e:
                logging.error(f"Error: {e}, attributes {name}")
