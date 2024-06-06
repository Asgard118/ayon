import os
import json
from ayon_api import get_addons_settings, get_addons_project_settings, get_bundles, get_project_anatomy_preset

os.environ['USE_AYON_SERVER'] = '1'
os.environ['AYON_SERVER_URL'] = 'http://192.168.0.102:5000'
os.environ['AYON_API_KEY'] = '9720fa2803bb488a84877038bdc6dda5'

from .auth import auth

auth.set_credentials('http://192.168.0.102:5000', '9720fa2803bb488a84877038bdc6dda5')

url_bund = f"{auth.SERVER_URL}/api/bundles"

BASE_URL = "http://192.168.0.102:5000"
API_KEY = '9720fa2803bb488a84877038bdc6dda5'

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
     
def get_bundles_list(bundle_name: str):
    data = get_bundles()
    if 'bundles' in data:
        for bundle in data['bundles']:
            if bundle['name'] == bundle_name:
                return bundle['addons']
    return None

def bundle_composition(name_bundle: str):
    return get_bundles(name_bundle)

def studio_settings_addons(bundle_name: str, file_path: str = None):
    data = get_addons_settings(bundle_name)
    if file_path is None:
        file_path = os.path.join(os.getcwd(), "settings.json")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def get_project_settings_addons(project_name: str, *args: str):
    data = get_addons_project_settings(project_name)
    if not args:
        return data
    
    for arg in args:
        if arg in data:
            data = data[arg]
    
    return data

def get_addons_setting(addon_name: str, name_project: str, name_budle: str):
    pro_data = get_addons_settings(project_name = name_project)
    studio_data = get_addons_settings(bundle_name = name_budle)
    return pro_data, studio_data[addon_name]

def get_anatomy_project():
    data = get_project_anatomy_preset()
    return data