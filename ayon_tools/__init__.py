import os
from .api.auth import StudioAuth

os.environ['USE_AYON_SERVER'] = '1'
self.studio_auth = StudioAuth('http://domain1.com', 'xxxxxx')