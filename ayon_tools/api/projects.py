import ayon_api

from ayon_tools.api.auth import Auth, default_auth


def get_project_names(auth) -> list:
    with auth:
        data = ayon_api.get_project_names()
    return data


def get_projects(auth: Auth = default_auth) -> list[dict]:
    with auth:
        data = ayon_api.get_projects()
    return data
