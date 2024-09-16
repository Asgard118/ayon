import ayon_api
import requests
from .auth import default_auth, Auth


# studio addon settings
def get_settings(
    bundle_name: str = None,
    variant: str = None,
    project_name: str = None,
    auth: Auth = default_auth,
) -> dict:
    """
    Универсальная функция, возвращает настройки аддонов исходя из указанных параметров
    относительно активных бандлов
    """
    with auth:
        data = ayon_api.get_addons_settings(
            bundle_name=bundle_name,
            variant=variant,
            project_name=project_name,
        )
    return data


def get_addon_studio_settings(
    addon_name: str, addon_version: str, variant: str, auth: Auth = default_auth
):
    """
    Возвращает студийные настройки конкретного аддона указанной версии вне зависимости от бандла
    """
    with auth:
        return ayon_api.get_addon_studio_settings(
            addon_name=addon_name,
            addon_version=addon_version,
            variant=variant,
        )


def get_addons_settings(
    bundle_name: str,
    variant: str,
    auth: Auth = default_auth,
):
    with auth:
        return ayon_api.get_addons_studio_settings(
            bundle_name=bundle_name, variant=variant
        )


def set_addon_studio_settings(
    addon_name: str,
    version: str,
    settings: dict,
    variant: str,
    auth: Auth = default_auth,
):
    """
    Обновление конкретной версии аддона, по определенным настройкам
    """
    with auth:
        ayon_api.post(
            f"/addons/{addon_name}/{version}/settings?variant={variant}", **settings
        )
    # response = requests.post(
    #     url=f"{auth.SERVER_URL}/api/addons/{addon_name}/{version}/settings?variant={variant}",
    #     headers=auth.HEADERS,
    #     json=settings,
    # )

    # response.raise_for_status()


# project settings
def get_project_settings(
    project_name: str,
    bundle_name: str,
    variant: str,
    auth: Auth = default_auth,
    **kwargs,
) -> dict:
    """
    Возвращает настройки аддонов конкретного проекта
    """
    with auth:
        data = ayon_api.get_addons_project_settings(
            project_name=project_name,
            bundle_name=bundle_name,
            variant=variant,
            **kwargs,
        )
    return data


def set_addon_project_settings(
    addon_name: str,
    version: str,
    project_name: str,
    variant: str,
    settings: dict,
    auth: Auth = default_auth,
):
    """
    Обновляет конкретную версию аддона проекта
    """

    response = requests.post(
        url=f"{auth.SERVER_URL}/api/addons/{addon_name}/{version}/settings/{project_name}?variant={variant}",
        headers=auth.HEADERS,
        json=settings,
    )
    response.raise_for_status()


def update_project(auth: Auth = default_auth, *args: any, **kwargs: any):
    with auth:
        return ayon_api.update_project(*args, **kwargs)


def install_addon(src_filepath, auth: Auth = default_auth):
    with auth:
        return ayon_api.upload_addon_zip(src_filepath)


def get_installed_addon_list(auth: Auth = default_auth):
    response = requests.get(
        url=f"{auth.SERVER_URL}/api/addons/install", headers=auth.HEADERS
    )
    return response.json()


def get_addon_default_settings(addon_name, addon_version, auth: Auth = default_auth):
    from ayon_tools.api.ayon_tools_addon import ayon_tools_url

    url = f"{auth.SERVER_URL}{ayon_tools_url(auth)}/{addon_name}/{addon_version}"
    resp = requests.get(url, headers=auth.HEADERS)
    resp.raise_for_status()
    return resp.json()
