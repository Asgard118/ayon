from ayon_tools.studio import StudioSettings
from collections.abc import Mapping
import json


def check_settings_match(studio: StudioSettings, **kwargs) -> bool:
    """
    Проверка соответствия настроек
    """
    # check anatomy
    is_match = True
    if not compare_dicts(studio.get_anatomy(), studio.get_rep_anatomy()):
        is_match = False
    # check bundle
    remote_bundle = (
        studio.get_productions_bundle()
        if not kwargs.get("stage")
        else studio.get_staging_bundle()
    )
    # check addons
    remote_addons = remote_bundle["addons"]
    local_addons = studio.get_rep_bundle()["addons"]
    if not compare_dicts(remote_addons, local_addons):
        is_match = False

    # check attributes
    if not compare_dicts(studio.get_attributes(), studio.get_rep_attributes()):
        is_match = False

    # check projects
    # TODO
    return is_match

def update_dict_with_changes(original: dict, updates: dict) -> dict:
    """
    Рекурсивно обновляет словарь original значениями из словаря updates.
    """
    for key, value in updates.items():
        if (
            isinstance(value, dict)
            and key in original
            and isinstance(original[key], dict)
        ):
            update_dict_with_changes(original[key], value)
        else:
            original[key] = value
    return original

def merge_dict(dict1, dict2):

    def is_dict(obj):
        return isinstance(obj, dict)

    def is_list(obj):
        return isinstance(obj, list)

    def merge_recursive(d1, d2):
        for key, value in d2.items():
            if key.endswith("+"):
                original_key = key[:-1]
                if original_key in d1:
                    if is_dict(d1[original_key]) and is_dict(value):
                        d1[original_key] = merge_recursive(d1[original_key], value)
                    elif is_list(d1[original_key]) and is_list(value):
                        d1[original_key].extend(value)
                    else:
                        raise TypeError(
                            f"Cannot merge {type(d1[original_key])} with {type(value)} for key {original_key}"
                        )
                else:
                    d1[original_key] = value
            elif key.endswith("-"):
                original_key = key[:-1]
                if original_key in d1:
                    if is_list(d1[original_key]) and is_list(value):
                        d1[original_key] = [
                            item for item in d1[original_key] if item not in value
                        ]
                    elif is_dict(d1[original_key]) and is_dict(value):
                        for k in value.keys():
                            if k in d1[original_key]:
                                del d1[original_key][k]
                    else:
                        raise TypeError(
                            f"Cannot perform difference on {type(d1[original_key])} with {type(value)} for key {original_key}"
                        )
            else:
                if key in d1:
                    if type(d1[key]) != type(value):
                        raise TypeError(
                            f"Type mismatch for key {key}: {type(d1[key])} != {type(value)}"
                        )
                    if is_dict(d1[key]) and is_dict(value):
                        d1[key] = merge_recursive(d1[key], value)
                    else:
                        d1[key] = value
                else:
                    d1[key] = value
        return d1

    return merge_recursive(dict1.copy(), dict2)


def compare_dicts(dict1: dict, dict2: dict):
    for key in dict2:
        if key not in dict1:
            return False
        if isinstance(dict2[key], dict) and isinstance(dict1[key], dict):
            if not compare_dicts(dict1[key], dict2[key]):
                return False
        elif dict1[key] != dict2[key]:
            return False
    return True