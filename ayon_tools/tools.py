from ayon_tools.studio import StudioSettings


def check_settings_match(studio: StudioSettings, **kwargs) -> bool:
    """
    Проверка соответствия настроек
    """
    # check anatomy
    is_match = True
    if not compare_dicts(studio.get_anatomy(), studio.get_actual_anatomy()):
        is_match = False
    # check bundle
    remote_bundle = (
        studio.get_productions_bundle()
        if not kwargs.get("stage")
        else studio.get_staging_bundle()
    )
    # check addons
    remote_addons = remote_bundle["addons"]
    local_addons = studio.get_actual_bundle()["addons"]
    if not compare_dicts(remote_addons, local_addons):
        is_match = False

    # check attributes
    if not compare_dicts(studio.get_attributes(), studio.get_actual_attributes()):
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
