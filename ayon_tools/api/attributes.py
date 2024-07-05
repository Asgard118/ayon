import re
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
    data.setdefault("deleteMissing", True)
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
    builtin: bool = False,
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


def validate_attributes(attributes: dict):
    errors = []
    for attribute in attributes:
        # name
        name = attribute.get("name")
        if not name:
            errors.append(f'Error attribute name "{name}": name is required')
        else:
            if not re.match(r"^[a-zA-Z_]{2,20}$", name):
                errors.append(
                    f'Error attribute name "{name}": '
                    f"name must be 2-20 characters long and contain only letters and underscores"
                )
        # scope
        scope = attribute.get("scope")
        if not scope:
            errors.append(f'Error attribute scope "{name}": scope is required')
        else:
            try:
                check_attr_scope(scope)
            except ValueError as e:
                errors.append(f'Error attribute scope "{name}": {e}')
        # data
        data = attribute.get("data")
        data_type = data.get("type")
        if data_type:
            try:
                _check_attr_date_type(data_type)
            except ValueError as e:
                errors.append(f'Error attribute data type "{name}": {e}')
    if errors:
        raise ValueError("\n".join(errors))


def update_default_data(attrib: dict):
    assert isinstance(attrib, dict)
    default_data = {
        "default": None,
        "description": None,
        "enum": None,
        "example": None,
        "ge": None,
        "gt": None,
        "inherit": True,
        "le": None,
        "lt": None,
        "maxItems": None,
        "maxLength": None,
        "minItems": None,
        "minLength": None,
        "regex": None,
    }
    for k, v in default_data.items():
        attrib["data"].setdefault(k, v)
    attrib.setdefault("builtin", False)
    return attrib


def merge_attributes(original_attr: dict, new_attr: dict):
    existing_attribs = {attr["name"]: attr for attr in original_attr["attributes"]}
    new_attr = {attr["name"]: attr for attr in new_attr["attributes"]}
    all_attrs = list({**existing_attribs, **new_attr}.values())
    all_attrs.sort(key=lambda attr: attr.get("position", 0))
    with_position = [attr for attr in all_attrs if attr.get("position")]
    without_position = [attr for attr in all_attrs if not attr.get("position")]
    max_pos = max(attr.get("position", 0) for attr in with_position)
    for i, attr in enumerate(without_position):
        attr["position"] = max_pos + i
        with_position.append(attr)
    return {"attributes": with_position}
