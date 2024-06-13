import os
os.environ['USE_AYON_SERVER'] = '1'
import ayon_api

__all__ = ['auth']


class Auth:
    endpoint_env_name = 'AYON_SERVER_URL'
    api_key_env_name = 'AYON_API_KEY'

    def __init__(self):
        self.SERVER_URL = None
        self.API_KEY = None
        self.HEADERS = {}
        self.set_credentials()

    def set_credentials(self, server_url: str = None, api_key: str = None):
        ayon_api.close_connection()
        server_url = server_url or os.getenv(self.endpoint_env_name)
        api_key = api_key or os.getenv(self.api_key_env_name)
        if not server_url or not api_key:
            return
        os.environ[self.endpoint_env_name] = self.SERVER_URL = server_url.rstrip('/')
        os.environ[self.api_key_env_name] = self.API_KEY = api_key
        self.HEADERS['x-api-key'] = self.API_KEY


auth = Auth()
