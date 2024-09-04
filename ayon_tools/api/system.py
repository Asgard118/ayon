from datetime import datetime

import requests
from .auth import default_auth, Auth
import ayon_api


def restart(auth: Auth = default_auth):
    with auth:
        ayon_api.trigger_server_restart()
    # response = requests.post(
    #     url=f"{auth.SERVER_URL}/api/system/restart", headers=auth.HEADERS
    # )
    # return response.raise_for_status()


def get_server_version(auth: Auth = default_auth):
    with auth:
        return ayon_api.get_server_version_tuple()


def get_events(
    topics: list[str],
    newer_than: datetime = None,
    older_than: datetime = None,
    auth: Auth = default_auth,
):
    if isinstance(newer_than, datetime):
        newer_than = newer_than.isoformat()
    if isinstance(older_than, datetime):
        older_than = older_than.isoformat()
    with auth:
        return ayon_api.get_events(topics, newer_than=newer_than, older_than=older_than)
