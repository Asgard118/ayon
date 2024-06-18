import ayon_api
import os
from ayon_api._api import GlobalContext

__all__ = ['Auth', 'default_auth']


class Auth:
    endpoint_env_name = 'AYON_SERVER_URL'
    api_key_env_name = 'AYON_API_KEY'

    def __init__(self, url: str = None, token: str = None):
        self.SERVER_URL = url
        self.API_KEY = token
        self.HEADERS = {}
        self._prev_connection = None
        self.set_credentials(url, token)

    def set_credentials(self, server_url: str = None, api_key: str = None):
        ayon_api.close_connection()
        server_url = server_url or os.getenv(self.endpoint_env_name)
        api_key = api_key or os.getenv(self.api_key_env_name)
        if not server_url or not api_key:
            return
        os.environ[self.endpoint_env_name] = self.SERVER_URL = server_url.rstrip('/')
        os.environ[self.api_key_env_name] = self.API_KEY = api_key
        self.HEADERS['x-api-key'] = self.API_KEY

    def __enter__(self):
        self._prev_connection = GlobalContext._connection
        if GlobalContext._connection and GlobalContext._connection._access_token != self.API_KEY:
            GlobalContext.change_token(self.SERVER_URL, self.API_KEY)

    def __exit__(self, exc_type, exc_val, exc_tb):
        GlobalContext._connection = self._prev_connection


default_auth = Auth()
