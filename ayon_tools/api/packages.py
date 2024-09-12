import json
import logging

import ayon_api
from ayon_api.exceptions import HTTPRequestError
from .auth import default_auth, Auth
from ..config import DEP_PACKAGES_DIR
from ..exceptipns import DepPackageNotExists, DepPackageAlreadyInstalled
from ayon_tools import tools


def get_dep_packages(auth: Auth = default_auth) -> dict:
    """
    Возвращает dependency packages на сервере
    """
    with auth:
        data = ayon_api.get_dependency_packages()
    return data


def upload_dep_package(archive: str, file_name: str, auth: Auth = default_auth):
    with auth:
        ayon_api.upload_dependency_package(archive, file_name)


def create_dep_packages(auth: Auth = default_auth, *args, **kwargs):
    with auth:
        ayon_api.create_dependency_package(*args, **kwargs)


def add_dep_package(filename, auth: Auth = default_auth):
    """
    Check if dep is not exist on server before use this function
    """
    arch, meta = get_dep_package_files(filename)

    with open(meta, "r") as f:
        data = json.load(f)
    if "size" in data:
        data["file_size"] = data.pop("size")
    if "platform" in data:
        data["platform_name"] = data.pop("platform")
    data.pop("bundle_name", None)

    try:
        with auth:
            logging.info(f'Add Dependency package {data["filename"]}')
            ayon_api.create_dependency_package(**data)
            ayon_api.upload_dependency_package(arch, data["filename"])
    except HTTPRequestError as e:
        if "409 Client Error: Conflict for url" in str(e):
            raise DepPackageAlreadyInstalled
        raise
    return data["filename"]


def remove_dep_package(filename, auth: Auth = default_auth):
    try:
        with auth:
            return ayon_api.delete_dependency_package(filename)
    except HTTPRequestError as e:
        if "Failed to delete dependency file" in str(e):
            raise DepPackageNotExists
        raise


def get_available_dep_package_list():
    """
    List of packages available on local workdir
    """
    return list(file.stem for file in DEP_PACKAGES_DIR.glob("*.zip"))


def get_dep_package_files(filename: str) -> (str, str):
    arch = next(DEP_PACKAGES_DIR.glob(f"{filename}.zip"), None)
    if arch is None:
        return download_dep_package(filename)
    meta = next(DEP_PACKAGES_DIR.glob(f"{filename}.zip.json"), None)
    if meta is None:
        raise ValueError(
            f"Dependency package {filename} not found in {DEP_PACKAGES_DIR}"
        )
    return arch, meta


def download_dep_package(package_name: str) -> (str, str):
    """
    Download dependency package from storage
    """
    raise NotImplementedError(
        f"Downloading not ready. Put built dep packages to folder {DEP_PACKAGES_DIR} (.zip and .zip.json)"
    )
    # TODO
    # return arch, meta


def get_package_meta_data(package_name: str):
    meta = next(DEP_PACKAGES_DIR.glob(f"{package_name}.zip.json"), None)
    if meta is None:
        raise FileNotFoundError(f"Meta data for dep {package_name} not found")
    with open(meta, "r") as f:
        return json.load(f)


def package_name_to_data(*package_names: str):
    """
    {
      "platform_name": "filename.zip"
    }
    """
    data = {}
    for package_name in package_names:
        meta = get_package_meta_data(package_name)
        data[meta["platform"]] = meta["filename"]
    return data
