from ayon_tools.studio import StudioSettings
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

def deep_compare(dict1, dict2):
    return json.dumps(dict1, sort_keys=True) == json.dumps(dict2, sort_keys=True)


def compare_dicts(dict1: dict, dict2: dict):
        return dict1 == dict2
    # if dict1.keys() != dict2.keys():
    #     return False
    #
    # for key in dict1:
    #     if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
    #         if not compare_dicts(dict1[key], dict2[key]):
    #             return False
    #     else:
    #         if dict1[key] != dict2[key]:
    #             return False
    #
    # return True


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


from collections.abc import Mapping


def compare_dicts_diff(dict1, dict2, path=""):
    differences = []

    def compare(v1, v2, path):
        if isinstance(v1, Mapping) and isinstance(v2, Mapping):
            for k in set(v1.keys()) | set(v2.keys()):
                if k not in v1:
                    differences.append(f"{path}{k}: Missing in first dictionary")
                elif k not in v2:
                    differences.append(f"{path}{k}: Missing in second dictionary")
                else:
                    compare(v1[k], v2[k], f"{path}{k}.")
        elif isinstance(v1, list) and isinstance(v2, list):
            if len(v1) != len(v2):
                differences.append(f"{path}: Lists have different lengths")
            for i, (item1, item2) in enumerate(zip(v1, v2)):
                compare(item1, item2, f"{path}[{i}].")
        elif v1 != v2:
            differences.append(f"{path[:-1]}: {v1} != {v2}")

    compare(dict1, dict2, path)
    return differences


