import ayon_api
from .auth import default_auth, Auth
import requests


class BundleVariant:
    PRODUCTION = "production"
    STAGING = "staging"


# bundles
def get_bundles(auth: Auth = default_auth) -> dict:
    with auth:
        data = ayon_api.get_bundles()
    return data


def get_bundle(bundle_name: str, auth: Auth = default_auth) -> dict:
    """
    Возвращает аддоны бандла по имени бандла
    # example
    {
                {
                'aftereffects': '0.1.3',
                'applications': '0.1.4',
                'blender': '0.1.6',
                'houdini': '0.2.11',
                'max': '0.1.5',
                'maya': '0.1.8',
                }
    }
    """
    with auth:
        data = get_bundles()
    if "bundles" in data:
        for bundle in data["bundles"]:
            if bundle["name"] == bundle_name:
                return bundle["addons"]


def get_production_bundle(auth: Auth = default_auth) -> dict:
    """
    Функция возвращает настройки бандла в статусе production
    """
    with auth:
        data = get_bundles().get("bundles", [])
    return next((item for item in data if item.get("isProduction")), None)


def get_staging_bundle(auth: Auth = default_auth) -> dict:
    """
    Возвращает бандл в статусе staging
    """
    with auth:
        data = get_bundles().get("bundles", [])
    return next((item for item in data if item.get("isStaging")), None)


def create_bundle(
    name: str,
    addons: dict,
    installer_version: str,
    auth: Auth = default_auth,
    **options,
):
    """
    Создает бандл, с указаным названием, аддонами и их версиями, и версией инсталера
    """
    with auth:
        ayon_api.create_bundle(
            name=name,
            addon_versions=addons,
            installer_version=installer_version,
            **options,
        )


def update_bundle(bundle_name: str, settings: dict, auth: Auth = default_auth):
    response = requests.patch(
        url=f"{auth.SERVER_URL}/api/bundles/{bundle_name}",
        headers=auth.HEADERS,
        json=settings,
    )
    response.raise_for_status()


def create_new_bundles(data: dict, bundle_name: str, auth: Auth = default_auth):
    data["activeUser"] = "admin"
    data["name"] = bundle_name
    response = requests.post(
        url=f"{auth.SERVER_URL}/api/bundles",
        headers=auth.HEADERS,
        json=data,
    )
    response.raise_for_status()
