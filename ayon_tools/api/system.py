import requests
from .auth import default_auth, Auth


def restart(auth: Auth = default_auth):
    response = requests.post(url=f'{auth.SERVER_URL}/api/system/restart', headers=auth.HEADERS)
    return response.raise_for_status()
