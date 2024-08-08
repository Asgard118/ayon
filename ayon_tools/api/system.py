import requests
from .auth import default_auth, Auth
import ayon_api


def restart(auth: Auth = default_auth):
    response = requests.post(url=f'{auth.SERVER_URL}/api/system/restart', headers=auth.HEADERS)
    return response.raise_for_status()

def get_server_info(auth: Auth = default_auth):
    return ayon_api.get_server_version()