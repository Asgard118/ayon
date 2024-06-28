from ayon_tools.studio import StudioSettings


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
        if isinstance(value, dict) and key in original and isinstance(original[key], dict):
            update_dict_with_changes(original[key], value)
        else:
            original[key] = value
    return original


def convert_bytes_to_str(data):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    elif isinstance(data, dict):
        return {k: convert_bytes_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_bytes_to_str(v) for v in data]
    else:
        return data