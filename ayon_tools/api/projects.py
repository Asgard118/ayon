import ayon_api
import requests
from ayon_tools.api.auth import Auth, default_auth


def get_project_names(auth) -> list:
    with auth:
        data = ayon_api.get_project_names()
    return data


def get_projects(auth: Auth = default_auth) -> list[dict]:
    with auth:
        data = ayon_api.get_projects()
    return data

def get_project_settings(status: str, project: str,auth: Auth = default_auth):
    response = requests.get(
        url=f"{auth.SERVER_URL}/api/settings?variant={status}&project_name={project}&summary=true",
        headers=auth.HEADERS,
    )
    data = response.json()
    return data