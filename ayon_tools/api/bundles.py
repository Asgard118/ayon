import ayon_api
from ayon_api import get_bundle_settings
from .auth import default_auth, Auth
import requests


class BundleMode:
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
        data = get_bundle_settings()
    return data


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
    dependency_packages=None,
    auth: Auth = default_auth,
):
    """
    Создает бандл, с указаным названием, аддонами и их версиями, и версией инсталера
    """
    with auth:
        ayon_api.create_bundle(
            name=name,
            addon_versions=addons,
            installer_version=installer_version,
            dependency_packages=dependency_packages,
        )


def update_bundle(bundle_name: str, settings: dict, auth: Auth = default_auth):
    response = requests.patch(
        url=f"{auth.SERVER_URL}/api/bundles/{bundle_name}",
        headers=auth.HEADERS,
        json=settings,
    )
    response.raise_for_status()
