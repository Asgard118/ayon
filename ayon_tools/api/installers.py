import json
import logging
import shutil
from pathlib import Path
import ayon_api
import requests
from ayon_tools.api.auth import Auth, default_auth
from ayon_tools.config import INSTALLERS_DIR
from ayon_tools.tools import download_file, get_json_file_content_by_url


def get_installer_name_list():
    return [f.name for f in INSTALLERS_DIR.glob("*.json")]


def installer_exists(installer_name, auth: Auth = default_auth):
    with auth:
        for inst in ayon_api.get_installers()["installers"]:
            if inst["filename"] == installer_name:
                return True
    return False


def download_and_install_installer(download_url, meta_data, auth: Auth):
    filename = Path(download_url).name
    local_file = Path(download_file(download_url, INSTALLERS_DIR / filename))
    logging.info(f"Download file... {filename} to {local_file}")
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


def download_installer_releases_by_tag(tag: str):  # not used
    assets_list = get_installers_download_urls(tag)
    if not assets_list:
        raise Exception("No assets found for this release.")

    download_dir: Path = INSTALLERS_DIR / tag
    download_dir.mkdir(exist_ok=True, parents=True)

    for asset in assets_list:
        file_name = asset["name"]
        file_path = download_dir / file_name
        if file_path.exists():
            if file_path.stat().st_size == asset["size"]:
                continue
            else:
                file_path.unlink()
        logging.info(f"Downloading installer file: {file_name}...")
        download_file(asset["url"], file_path)

    return download_dir


def get_installers_download_urls(tag: str):
    """
    return [
        {filename: filenme, url: url, size: 000},
        ...
    ]

    """
    url = f"https://api.github.com/repos/ynput/ayon-launcher/releases/tags/{tag}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to get release info {tag}: {response.status_code}")

    assets_data = response.json().get("assets", [])
    unique_set = set()
    assets_data.sort(key=lambda x: x["name"], reverse=True)
    json_files = [x for x in assets_data if Path(x["name"]).suffix == ".json"]
    if not json_files:
        raise Exception("json files not found")

    for json_file in json_files:
        asset_data = get_json_file_content_by_url(json_file["browser_download_url"])
        key = (asset_data["version"], asset_data["platform"])
        if key in unique_set:
            continue
        unique_set.add(key)
        yield {
            "url": json_file["browser_download_url"].rsplit(".", 1)[0],
            "name": json_file["name"].rsplit(".", 1)[0],
            "size": json_file["size"],
            "json": asset_data,
        }


def cleanup_installer_dir():
    if INSTALLERS_DIR.exists():
        shutil.rmtree(INSTALLERS_DIR)
