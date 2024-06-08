import os
os.environ['USE_AYON_SERVER'] = '1'
os.environ['AYON_SERVER_URL'] = 'http://192.168.0.102:5000'
os.environ['AYON_API_KEY'] = '9720fa2803bb488a84877038bdc6dda5'

from ayon_tools import ayon_func

ayon_func.get_bundles()


