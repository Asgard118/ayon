import json
import logging
from pathlib import Path

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
    # from pprint import pprint
    # print('='*50)
    # print(repr(dict(
    #     name=name,
    #     addons=addons,
    #     installer_version=installer_version,
    #     **options
    # )))
    # print('='*50)
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


def installer_exists(installer_name, auth: Auth = default_auth):
    with auth:
        for inst in ayon_api.get_installers()["installers"]:
            if inst["filename"] == installer_name:
                return True
    return False


def download_and_install_installer(download_url, meta_data, auth: Auth):
    from ayon_tools.tools import download_file_to_temp

    logging.info(
        f"Download file... {Path(download_url).name}",
    )
    local_file = Path(download_file_to_temp(download_url))
    with auth:
        logging.info(f"Upload meta file for {local_file.name}")
        resp = ayon_api.get_server_api_connection().post(
            "desktop/installers", **meta_data
        )
        resp.raise_for_status()

        logging.info("Upload installer file...")
        ayon_api.upload_installer(local_file.as_posix(), local_file.name)


def upload_installer(installer_file, meta_file, auth: Auth, reinstall=False):
    installer_file = Path(installer_file)
    assert installer_file.exists(), "Installer file not found"
    meta_file = Path(meta_file)
    assert meta_file.exists(), "Meta file not found"
    with meta_file.open() as f:
        installer_data = json.load(f)
    # check is installed
    if installer_exists(installer_file.name, auth):
        if reinstall:
            ayon_api.delete_installer(installer_file.name)
        else:
            logging.info(f"Installer {installer_file.name} already exists")
            return
    # install
    with auth:
        logging.info(f"Upload meta file for {installer_data['filename']}")
        resp = ayon_api.get_server_api_connection().post(
            "desktop/installers", **installer_data
        )
        resp.raise_for_status()

        logging.info("Upload installer file ")
        ayon_api.upload_installer(installer_file.as_posix(), installer_file.name)


def remove_installer(name: str, auth: Auth):
    with auth:
        ayon_api.delete_installer(name)
