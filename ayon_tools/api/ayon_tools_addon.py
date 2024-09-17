import logging

import ayon_api
from ayon_tools.api.auth import Auth


def is_installed(auth: Auth, version: str = None) -> bool:
    with auth:
        addons = ayon_api.get_addons_info()
    for addon in addons["addons"]:
        if addon["name"] == "ayon_tools":
            if not version:
                return True
            if version in addon["versions"].keys():
                return True
    return False


def get_installed_versions(auth: Auth) -> list:
    with auth:
        addons = ayon_api.get_addons_info()
    for addon in addons["addons"]:
        if addon["name"] == "ayon_tools":
            return list(addon["versions"].keys())


def ayon_tools_url(auth: Auth):
    version = get_installed_versions(auth)
    if version:
        return f"addons/ayon_tools/{sorted(version)[-1]}"
    raise Exception("ayon_tools is not installed")


def install(studio: "StudioSettings"):
    from ayon_tools.base_addon import Addon

    addon = Addon("ayon_tools", studio)
    versions = addon.get_versions()
    if not versions:
        raise Exception("No versions found for ayon_tools")
    logging.info(f"Install ayon_tools v{versions[-1]}")
    studio.install_addon(addon.name, versions[-1])
    studio.restart_server()


def ensure_installed(studio: "StudioSettings", version: str = None):
    if not is_installed(studio.auth, version):
        logging.info("Install ayon_tools...")
        install(studio)
    else:
        logging.info("ayon_tools is already installed")


# endpoints


def get_addon_default_settings(addon_name, addon_version, auth: Auth):
    url = f"{ayon_tools_url(auth)}/addon-default-settings/{addon_name}/{addon_version}"
    with auth:
        resp = ayon_api.get(url, auth=auth)
    resp.raise_for_status()
    return resp.orig_response.json()


def ping(auth: Auth):
    try:
        with auth:
            ayon_api.get(f"{ayon_tools_url(auth)}/ping", auth=auth)
    except Exception:
        return False
