import requests
from .auth import auth

def restart():
	response = requests.post(url=f'{auth.SERVER_URL}/api/system/restart', headers=auth.HEADERS)
	return response.raise_for_status()